$('img.modal-img').each(function() {
    var modal = $('<div class="img-modal"><span>&times;</span><img /><div></div></div>');
    modal.find('img').attr('src', $(this).attr('src'));
    if($(this).attr('alt'))
      modal.find('div').text($(this).attr('alt'));
    $(this).after(modal);
    modal = $(this).next();
    $(this).click(function(event) {
      modal.show(300);
      modal.find('span').show(0.3);
    });
    modal.find('span').click(function(event) {
      modal.hide(300);
    });
  });
  $(document).keyup(function(event) {
    if(event.which==27)
      $('.img-modal>span').click();
  });