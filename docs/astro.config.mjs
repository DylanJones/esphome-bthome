import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://dz0ny.github.io',
  base: '/esphome-bthome',
  integrations: [
    starlight({
      title: 'ESPHome BTHome',
      description: 'BTHome v2 BLE Protocol Component for ESPHome',
      social: {
        github: 'https://github.com/dz0ny/esphome-bthome',
      },
      sidebar: [
        {
          label: 'Getting Started',
          autogenerate: { directory: 'getting-started' },
        },
        {
          label: 'Configuration',
          autogenerate: { directory: 'configuration' },
        },
        {
          label: 'Platforms',
          autogenerate: { directory: 'platforms' },
        },
        {
          label: 'Devices',
          autogenerate: { directory: 'devices' },
        },
        {
          label: 'Reference',
          autogenerate: { directory: 'reference' },
        },
      ],
      editLink: {
        baseUrl: 'https://github.com/dz0ny/esphome-bthome/edit/main/docs/',
      },
      customCss: ['./src/styles/custom.css'],
    }),
  ],
});
