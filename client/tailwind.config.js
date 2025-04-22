import { contentPath, skeleton } from "@skeletonlabs/skeleton/plugin";
import * as themes from "@skeletonlabs/skeleton/themes";
import forms from "@tailwindcss/forms";

export default {
  content: [
    "./src/**/*.{html,js,svelte,ts}",
    contentPath(import.meta.url, "svelte"),
  ],
  theme: {
    extend: {},
  },
  plugins: [
    forms,
    skeleton({
      themes: [themes.cerberus,
              themes.mint, 
              themes.catppuccin,
              themes.vintage,
              themes.fennec,
              themes.rocket,
              themes.seafoam,
              themes.pine,
              themes.nouveau,
              themes.reign,
              themes.vox,],
    }),
  ],
};
