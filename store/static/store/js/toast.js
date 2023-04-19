function btnfire() {
  Swal.fire({
  icon: "error",
  title: "برای ادامه و مشاهده لینک دانلود اشتراک تهیه کنید",
  text: "شما اشتراک فعالی ندارید",
  footer: '<a href="http://127.0.0.1:8000/movie/package/buy/">خرید اشتراک</a>',
  showConfirmButton : false  ,
});
}


function wellcome() {
  Swal.fire({
  position: 'top-start',
  width : 650,
  icon: 'success',
  title: 'با موفقیت وارد شدید',
  showConfirmButton: false,
  timer: 1500,
})
}


$(document).ready(function () {
  if (!document.cookie.loggedIn){
    wellcome();
  }
});

