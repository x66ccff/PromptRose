import { e as escape_html } from "../../chunks/escaping.js";
import "clsx";
import { c as pop, p as push } from "../../chunks/index.js";
import "@tauri-apps/api/core";
const replacements = {
  translate: /* @__PURE__ */ new Map([
    [true, "yes"],
    [false, "no"]
  ])
};
function attr(name, value, is_boolean = false) {
  if (is_boolean || name === "class") return "";
  const normalized = name in replacements && replacements[name].get(value) || value;
  const assignment = is_boolean ? "" : `="${escape_html(normalized, true)}"`;
  return ` ${name}${assignment}`;
}
function _page($$payload, $$props) {
  push();
  let name = "";
  let greetMsg = "";
  $$payload.out += `<main class="container svelte-16feo4b"><h1 class="svelte-16feo4b">Welcome to Tauri + Svelte</h1> <div class="row svelte-16feo4b"><a href="https://vitejs.dev" target="_blank" class="svelte-16feo4b"><img src="/vite.svg" class="logo vite svelte-16feo4b" alt="Vite Logo"></a> <a href="https://tauri.app" target="_blank" class="svelte-16feo4b"><img src="/tauri.svg" class="logo tauri svelte-16feo4b" alt="Tauri Logo"></a> <a href="https://kit.svelte.dev" target="_blank" class="svelte-16feo4b"><img src="/svelte.svg" class="logo svelte-kit svelte-16feo4b" alt="SvelteKit Logo"></a></div> <p>Click on the Tauri, Vite, and SvelteKit logos to learn more.</p> <form class="row svelte-16feo4b"><input id="greet-input" placeholder="Enter a name..."${attr("value", name)} class="svelte-16feo4b"> <button type="submit" class="svelte-16feo4b">Greet</button></form> <p>${escape_html(greetMsg)}</p></main>`;
  pop();
}
export {
  _page as default
};
