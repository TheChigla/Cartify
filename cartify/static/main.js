let navCartBtn = document.querySelector('.header__cart---button');
let navCartPopup = document.querySelector('.header__cart---popup-wrapper');
let navAccountPopup = document.querySelector(
  '.header__account---popup-wrapper'
);
let alert = document.querySelector('.auth__alert');
let closeAlertBtn = document.querySelector('.auth__alert---close-btn');

//  Navbar categories popup menu
document.addEventListener('click', (e) => {
  if (
    e.target.classList.contains('header__search---dropdown-flex') ||
    e.target.classList.contains('header__search---dropdown-icon') ||
    e.target.classList.contains('header__search---dropdown-span')
  ) {
    document
      .querySelector('.header__search---dropdown-content')
      .classList.toggle('fadeFromTop');
  } else if (!e.target.classList.contains('header__search---dropdown-item')) {
    document
      .querySelector('.header__search---dropdown-content')
      .classList.remove('fadeFromTop');
  }
});

//  Navbar cart popup menu
document.addEventListener('mousemove', (e) => {
  if (
    e.target.classList.contains('header__cart---button') ||
    e.target.classList.contains('header__cart---icon') ||
    e.target.classList.contains('header__cart---icon-img') ||
    e.target.classList.contains('header__cart---count') ||
    e.target.classList.contains('header__count---label') ||
    e.target.classList.contains('header__cart---popup') ||
    e.target.classList.contains('header__cart---popup-wrapper') ||
    e.target.classList.contains('header__cart---popup-items') ||
    e.target.classList.contains('header__cart---popup-item') ||
    e.target.classList.contains('header__cart---popup-item-img') ||
    e.target.classList.contains('header__cart---popup-item-image') ||
    e.target.classList.contains('header__cart---popup-item-details') ||
    e.target.classList.contains('header__cart---popup-item-details__body') ||
    e.target.classList.contains('header__cart---popup-item-name') ||
    e.target.classList.contains('header__cart---popup-item-price') ||
    e.target.classList.contains('header__cart---popup-item-close') ||
    e.target.classList.contains('header__cart---popup-item-close__icon') ||
    e.target.classList.contains('header__cart---popup-total') ||
    e.target.classList.contains('header__cart---popup-total__label') ||
    e.target.classList.contains('header__cart---popup-total__count') ||
    e.target.classList.contains('header__cart---popup-actions') ||
    e.target.classList.contains('header__cart---popup-btn')
  ) {
    navCartPopup.classList.add('fadeFromDown');
  } else {
    navCartPopup.classList.remove('fadeFromDown');
  }
});

//  Navbar cart account menu
document.addEventListener('mousemove', (e) => {
  if (
    e.target.classList.contains('header__account---button') ||
    e.target.classList.contains('header__account---icon') ||
    e.target.classList.contains('header__account---icon-img') ||
    e.target.classList.contains('header__account---label') ||
    e.target.classList.contains('header__account---popup') ||
    e.target.classList.contains('header__account---popup-wrapper') ||
    e.target.classList.contains('header__account---popup-items') ||
    e.target.classList.contains('header__account---popup-item') ||
    e.target.classList.contains('header__account---popup-item-link') ||
    e.target.classList.contains('header__account---popup-item-icon') ||
    e.target.classList.contains('header__account---popup-item-img')
  ) {
    navAccountPopup.classList.add('fadeFromDown');
  } else {
    navAccountPopup.classList.remove('fadeFromDown');
  }
});

// Close alert
closeAlertBtn.addEventListener('click', () => {
  alert.style.display = 'none';
});
