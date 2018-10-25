import torch
import torch.nn as nn
import torch.nn.functional as F

import numpy as np

def layer_init(layer):
    nn.init.xavier_normal_(layer.weight.data)
    nn.init.constant_(layer.bias.data, 0)
    return layer

    
class FCBody(nn.Module):
    def __init__(self, state_dim, hidden_units=(64, 96, 128), gate=F.relu):
        super(FCBody, self).__init__()
        dims = (state_dim,) + hidden_units
        self.layers = nn.ModuleList([layer_init(nn.Linear(dims[j-1], dims[j])) for j in range(1, len(dims))])
        self.gate = gate
        self.feature_dim = dims[-1]

    def forward(self, x):
        for layer in self.layers:
            x = self.gate(layer(x))
        return x
    
        
class ActorCriticNet(nn.Module):
    def __init__(self, state_dim, action_dim, actor_body, critic_body, phi_body=None):
        super(ActorCriticNet, self).__init__()
        if actor_body is None: actor_body = FCBody(phi_body.feature_dim)
        if critic_body is None: critic_body = FCBody(phi_body.feature_dim)
        self.phi_body = phi_body
        self.actor_body = actor_body
        self.critic_body = critic_body
        self.fc_action = layer_init(nn.Linear(actor_body.feature_dim, action_dim))
        self.fc_critic = layer_init(nn.Linear(critic_body.feature_dim, 1))

        self.actor_params = list(self.actor_body.parameters()) + list(self.fc_action.parameters())
        self.critic_params = list(self.critic_body.parameters()) + list(self.fc_critic.parameters())
        if self.phi_body is not None: 
            self.phi_params = list(self.phi_body.parameters())
        else:
            self.phi_params = None
  
        
class GaussianActorCriticNet(nn.Module):
    def __init__(self,
                 device,
                 state_dim,
                 action_dim,
                 actor_body=None,
                 critic_body=None,
                 phi_body=None):
        super(GaussianActorCriticNet, self).__init__()
        self.network = ActorCriticNet(state_dim, action_dim, actor_body, critic_body, phi_body)
        self.std = nn.Parameter(torch.ones(1, action_dim))
        self.to(device)

    def forward(self, obs, action=None):
        #obs = tensor(obs)
        a_est, v_est = None, None
        if self.network.phi_body is not None:
            phi = self.network.phi_body(obs)
            a_est = self.network.actor_body(phi)
            phi_v = self.network.critic_body(phi)
        else:
            a_est = self.network.actor_body(obs)
            v_est = self.network.critic_body(obs)
        #print('A est {} v est {}'.format(a_est.size(), v_est.size()))
        mean = torch.tanh(self.network.fc_action(a_est))
        #print('Mean size ', mean.size())
        v = self.network.fc_critic(v_est)
        dist = torch.distributions.Normal(mean, self.std.data)
        if action is None:
            action = dist.sample()
        log_prob = dist.log_prob(action)
        log_prob = torch.sum(log_prob, dim=1, keepdim=True)
        return action, log_prob, torch.tensor(np.zeros((log_prob.size(0), 1))), v
    

# print('State shape ', states.shape, state_size)
# s0 = states[0]
# print('s0 type ', type(s0), s0.shape)
# print(np.vstack(states).shape)
# torch_states = torch.from_numpy(np.vstack(states)).float()
# print(torch_states.size())


# actor_net = FCBody(state_size)
# features = actor_net(torch_states)
# print('Feature size ', features.size())


# actor_critic_net = ActorCriticNet(state_size, action_size, FCBody(state_size), FCBody(state_size), phi_body=None)
# # a_est = actor_critic_net.actor_body(torch_states)
# # v_est = actor_critic_net.critic_body(torch_states)
# # a_est = actor_critic_net.fc_action(a_est)
# # v_est = actor_critic_net.fc_critic(v_est)
# # print('Action ests size ', a_est.size())

# # std = torch.ones(1, action_size)
# # mean = torch.tanh(a_est)
# # print('Mean {}, std {}'.format(mean[:3], std))

# # dist = torch.distributions.Normal(mean, std)
# # action = dist.sample()
# # print('sample action size {}, \n{}'.format(action.size(), action))
# # log_prob = dist.log_prob(action)
# # print('Log prob ', log_prob.size(), log_prob)
# # # if action is None:
# # #     action = dist.sample()
# # # log_prob = dist.log_prob(action)
# # # log_prob = torch.sum(log_prob, dim=1, keepdim=True)
# # torch.tensor(np.zeros((log_prob.size(0), 1)))

# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# actor_critic_net = GaussianActorCriticNet(device, state_size, action_size, FCBody(state_size), FCBody(state_size), phi_body=None)
# action, log_prob, what, v = actor_critic_net(torch_states)