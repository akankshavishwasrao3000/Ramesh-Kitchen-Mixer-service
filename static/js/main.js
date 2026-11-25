(function () {
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function setUpAmbientVisual() {
    const ambient = document.createElement("div");
    ambient.className = "ambient-visual";
    ambient.setAttribute("aria-hidden", "true");
    document.body.appendChild(ambient);
  }

  function setUpProgress() {
    const progress = document.createElement("div");
    const fill = document.createElement("span");
    progress.className = "scroll-progress";
    progress.setAttribute("aria-hidden", "true");
    progress.appendChild(fill);
    document.body.appendChild(progress);

    const update = () => {
      const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
      fill.style.transform = `scaleX(${maxScroll > 0 ? window.scrollY / maxScroll : 0})`;
    };
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  function setUpCursor() {
    if (reducedMotion || !window.matchMedia("(pointer: fine)").matches) return;

    const dot = document.createElement("span");
    const ring = document.createElement("span");
    dot.className = "scroll-cursor";
    ring.className = "scroll-cursor-ring";
    dot.setAttribute("aria-hidden", "true");
    ring.setAttribute("aria-hidden", "true");
    document.body.append(dot, ring);

    document.addEventListener("pointermove", (event) => {
      dot.style.opacity = "1";
      ring.style.opacity = "1";
      dot.style.transform = `translate3d(${event.clientX - 2.5}px, ${event.clientY - 2.5}px, 0)`;
      ring.style.transform = `translate3d(${event.clientX - 14}px, ${event.clientY - 14}px, 0)`;
    });

    document.querySelectorAll("a, button, .product-card, summary").forEach((item) => {
      item.addEventListener("pointerenter", () => ring.classList.add("is-active"));
      item.addEventListener("pointerleave", () => ring.classList.remove("is-active"));
    });
  }

  function setUpReveals() {
    const revealSelector = [
      ".reveal-item",
      "[data-reveal]",
      ".page-content > section",
      ".page-content .contact-card",
      ".page-content .feature-card",
      ".page-content .info-card",
      ".page-content .step-card",
      ".page-content .policy-section",
      ".page-content .stat-card",
      ".page-content .product-card-item",
      ".page-content .table-section",
      ".page-content .section-card",
      ".page-content .contact-card",
      ".page-content .feature-card",
      ".page-content .service-card",
      ".page-content .order-item",
      ".page-content .repair-item",
      ".page-content .card",
      ".page-content > .services-page",
      ".page-content > .container",
      ".page-content > .container-fluid",
      ".page-content > .bg-light",
      ".page-content > .user-detail-header"
    ].join(",");
    const items = [...document.querySelectorAll(revealSelector)];
    items.forEach((item) => item.classList.add("reveal-item"));

    if (reducedMotion) {
      items.forEach((item) => item.classList.add("is-visible"));
      return;
    }

    if (window.gsap && window.ScrollTrigger) {
      window.gsap.registerPlugin(window.ScrollTrigger);
      items.forEach((item, index) => {
        window.gsap.fromTo(item, { autoAlpha: 0, y: 24 }, {
          autoAlpha: 1,
          y: 0,
          duration: 0.65,
          delay: (index % 4) * 0.055,
          ease: "power2.out",
          onStart: () => item.classList.add("is-visible"),
          scrollTrigger: { trigger: item, start: "top 88%", once: true }
        });
      });
      return;
    }

    if (!("IntersectionObserver" in window)) {
      items.forEach((item) => item.classList.add("is-visible"));
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -24px 0px" });

    items.forEach((item) => observer.observe(item));
  }

  function setUpScrollEffects() {
    const header = document.querySelector(".site-header");
    if (header) {
      const updateHeader = () => header.classList.toggle("is-scrolled", window.scrollY > 24);
      window.addEventListener("scroll", updateHeader, { passive: true });
      updateHeader();
    }

    if (window.gsap && window.ScrollTrigger && !reducedMotion) {
      window.gsap.registerPlugin(window.ScrollTrigger);
      window.gsap.utils.toArray("[data-parallax]").forEach((element) => {
        window.gsap.to(element, {
          yPercent: -8,
          ease: "none",
          scrollTrigger: { trigger: element, start: "top bottom", end: "bottom top", scrub: 0.6 }
        });
      });
      if (window.matchMedia("(min-width: 1100px)").matches) {
        window.gsap.utils.toArray("[data-pin]").forEach((element) => {
          window.ScrollTrigger.create({
            trigger: element,
            start: "top top+=100",
            end: "+=160",
            pin: element,
            pinSpacing: true
          });
        });
      }
    }
  }

  function setUpPolicyToc() {
    const firstSection = document.querySelector(".policy-section");
    const sections = [...document.querySelectorAll(".policy-section h3")];
    if (!firstSection || sections.length < 2) return;

    const nav = document.createElement("nav");
    const list = document.createElement("ol");
    nav.className = "policy-toc";
    nav.setAttribute("aria-label", "Policy contents");
    const heading = document.createElement("strong");
    heading.textContent = "On this page";
    nav.appendChild(heading);

    sections.forEach((sectionHeading, index) => {
      const section = sectionHeading.closest(".policy-section");
      if (!section.id) section.id = `policy-section-${index + 1}`;
      const item = document.createElement("li");
      const link = document.createElement("a");
      link.href = `#${section.id}`;
      link.textContent = sectionHeading.textContent.trim();
      item.appendChild(link);
      list.appendChild(item);
    });

    nav.appendChild(list);
    firstSection.parentNode.insertBefore(nav, firstSection);
  }

  function setUpButtons() {
    if (reducedMotion) return;
    document.querySelectorAll(".btn").forEach((button) => {
      button.addEventListener("pointermove", (event) => {
        if (event.pointerType !== "mouse") return;
        const bounds = button.getBoundingClientRect();
        const offsetX = (event.clientX - bounds.left - bounds.width / 2) / bounds.width;
        const offsetY = (event.clientY - bounds.top - bounds.height / 2) / bounds.height;
        button.style.translate = `${offsetX * 5}px ${offsetY * 4}px`;
      });
      button.addEventListener("pointerleave", () => { button.style.translate = ""; });
      button.addEventListener("click", (event) => {
        const bounds = button.getBoundingClientRect();
        const ripple = document.createElement("span");
        ripple.className = "ripple-effect";
        ripple.style.left = `${event.clientX - bounds.left}px`;
        ripple.style.top = `${event.clientY - bounds.top}px`;
        button.appendChild(ripple);
        ripple.addEventListener("animationend", () => ripple.remove(), { once: true });
      });
    });
  }

  function setUpParticles() {
    if (reducedMotion) return;
    const particles = document.createElement("div");
    particles.className = "page-particles";
    particles.setAttribute("aria-hidden", "true");
    particles.innerHTML = "<span></span><span></span><span></span>";
    document.body.appendChild(particles);
  }

  function setUpMobileNav() {
    const menu = document.getElementById("mainNavbar");
    if (!menu) return;

    menu.addEventListener("shown.bs.collapse", () => {
      document.body.classList.add("nav-open");
    });
    menu.addEventListener("hidden.bs.collapse", () => {
      document.body.classList.remove("nav-open");
    });
    document.addEventListener("click", (event) => {
      const toggler = document.querySelector(".navbar-toggler");
      if (menu.classList.contains("show") && !menu.contains(event.target) && !toggler?.contains(event.target) && window.bootstrap?.Collapse) {
        window.bootstrap.Collapse.getOrCreateInstance(menu).hide();
      }
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && menu.classList.contains("show") && window.bootstrap?.Collapse) {
        window.bootstrap.Collapse.getOrCreateInstance(menu).hide();
      }
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.documentElement.classList.add("motion-ready");
    setUpAmbientVisual();
    setUpProgress();
    setUpCursor();
    setUpReveals();
    setUpScrollEffects();
    setUpButtons();
    setUpParticles();
    setUpPolicyToc();
    setUpMobileNav();
  });
})();
