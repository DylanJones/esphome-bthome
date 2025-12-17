import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightThemeNext from 'starlight-theme-next';
import mermaid from 'astro-mermaid';

export default defineConfig({
  site: 'https://dz0ny.github.io',
  base: '/esphome-bthome',
  integrations: [
    mermaid({
      theme: 'neutral',
      autoTheme: true,
    }),
    starlight({
      plugins: [starlightThemeNext()],
      title: 'ESPHome BTHome',
      description: 'BTHome v2 BLE Protocol Component for ESPHome',
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/dz0ny/esphome-bthome' },
      ],
      expressiveCode: {
        themes: ['github-dark', 'github-light'],
        defaultProps: {
          wrap: true,
        },
        styleOverrides: {
          borderRadius: '0.5rem',
          codePaddingBlock: '0.75rem',
          codePaddingInline: '1rem',
        },
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
          label: 'Components',
          autogenerate: { directory: 'components' },
        },
        {
          label: 'Platforms',
          autogenerate: { directory: 'platforms' },
        },
        {
          label: 'Tools',
          autogenerate: { directory: 'tools' },
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
