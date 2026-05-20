# Jam Mission – Holistic Off‑Grid Experiences

Jam Mission offers a curated collection of sustainable, off‑grid experiences and products. This repository contains a static web front‑end built with plain HTML, CSS and a touch of JavaScript. It is designed to be immediately deployable on platforms like Vercel or Netlify without additional build steps.

## Features

- **Modern glassmorphism design** inspired by high‑tech Apple Glass UI, with eco‑sustainable colours and transparency effects.
- **Landing page** showcasing all services with images and descriptions.
- **Dedicated service pages** for boondocking, pet glamping, petting zoo, nature tours, workshops & camps, campsites, and farm products (goats & eggs).
- **Cart page** with sample items and checkout button.
- **Contact page** with a simple form.
- **Owner and Admin login pages** for future integrations.
- **Responsive layout** that adapts to mobile and desktop.
- **Credential file** (`credentials.txt`, ignored by Git) containing sample usernames, IDs and passwords for owner and admin.

## Directory Structure

```
jam_house_site/
│  index.html            # landing page
│  style.css             # shared styles
│  .gitignore            # ignores credentials.txt
│  credentials.txt       # sample secret credentials (not to be committed)
│
├─ services/             # service-specific pages
│   ├─ boondocking.html
│   ├─ pet_glamping.html
│   ├─ petting_zoo.html
│   ├─ nature_tours.html
│   ├─ workshops.html
│   ├─ campsites.html
│   └─ goats_eggs.html
│
├─ images/               # placeholder images (AI‑generated)
│   ├─ boondocking.png
│   ├─ pet_glamping.png
│   ├─ petting_zoo.png
│   ├─ nature_tours.png
│   ├─ workshops.png
│   ├─ campsites.png
│   └─ goats_eggs.png
│
├─ cart/
│   └─ cart.html         # cart placeholder
│
├─ contact/
│   └─ contact.html      # contact form
│
└─ login/
    ├─ owner_login.html
    └─ admin_login.html
```

## Deployment

This site is static and requires no server‑side code. To deploy on [Vercel](https://vercel.com/):

1. **Create a new project** and import this repository from GitHub (or upload the folder directly).
2. **Select “Other”** as the framework. Vercel will detect that no build step is needed.
3. **Deploy**. The default root directory (`jam_house_site`) contains all static files. Ensure that Vercel points to this directory if you import the entire repository.
4. After deployment, your site will be accessible at `https://<your‑project>.vercel.app`.

Alternatively, you can drag‑and‑drop the contents of `jam_house_site` into Vercel’s “Deploy” section, which will automatically create and deploy a new project.

## Customization

- Replace the placeholder images in `images/` with your own photos. Keep the filenames or update the `<img>` tags accordingly.
- Edit the text in the HTML files to reflect your actual offerings, pricing, and descriptions.
- Integrate real authentication and back‑end functionality as needed. The login and cart pages are placeholders.
- Update the `credentials.txt` file with actual credentials if desired. This file is ignored by Git by default.

## Contact

Feel free to reach out via the contact form on the website or by emailing the Jam Mission team at `thejammission@gmail.com`.

We hope this template helps you launch your mission and share your vision with the world!