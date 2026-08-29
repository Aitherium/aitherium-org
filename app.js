/* Aitherium Foundation — aitherium.org
   Minimal progressive enhancement: mobile nav toggle only.
   The site is fully readable with JS off. */
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle')
  const links = document.getElementById('nav-links')
  if (!toggle || !links) return

  toggle.addEventListener('click', () => {
    const open = links.classList.toggle('open')
    toggle.setAttribute('aria-expanded', String(open))
  })

  // Close the menu when a link is chosen
  links.addEventListener('click', e => {
    if (e.target.closest('a')) {
      links.classList.remove('open')
      toggle.setAttribute('aria-expanded', 'false')
    }
  })
})
