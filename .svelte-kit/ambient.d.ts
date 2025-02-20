
// this file is generated — do not edit it


/// <reference types="@sveltejs/kit" />

/**
 * Environment variables [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env`. Like [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private), this module cannot be imported into client-side code. This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured).
 * 
 * _Unlike_ [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private), the values exported from this module are statically injected into your bundle at build time, enabling optimisations like dead code elimination.
 * 
 * ```ts
 * import { API_KEY } from '$env/static/private';
 * ```
 * 
 * Note that all environment variables referenced in your code should be declared (for example in an `.env` file), even if they don't have a value until the app is deployed:
 * 
 * ```
 * MY_FEATURE_FLAG=""
 * ```
 * 
 * You can override `.env` values from the command line like so:
 * 
 * ```bash
 * MY_FEATURE_FLAG="enabled" npm run dev
 * ```
 */
declare module '$env/static/private' {
	export const LESSOPEN: string;
	export const CONDA_PROMPT_MODIFIER: string;
	export const OPENROUTER_API_KEY: string;
	export const RUC_KEY: string;
	export const SSH_CLIENT: string;
	export const USER: string;
	export const npm_config_user_agent: string;
	export const GIT_ASKPASS: string;
	export const XDG_SESSION_TYPE: string;
	export const npm_node_execpath: string;
	export const BROWSER: string;
	export const LD_LIBRARY_PATH: string;
	export const SHLVL: string;
	export const TAURI_PLATFORM_VERSION: string;
	export const npm_config_noproxy: string;
	export const CONDA_SHLVL: string;
	export const HOME: string;
	export const OLDPWD: string;
	export const TERM_PROGRAM_VERSION: string;
	export const VSCODE_IPC_HOOK_CLI: string;
	export const npm_package_json: string;
	export const TAURI_ARCH: string;
	export const VSCODE_GIT_ASKPASS_MAIN: string;
	export const SSL_CERT_FILE: string;
	export const VSCODE_GIT_ASKPASS_NODE: string;
	export const npm_config_local_prefix: string;
	export const npm_config_userconfig: string;
	export const DBUS_SESSION_BUS_ADDRESS: string;
	export const TAURI_PLATFORM_TYPE: string;
	export const VISUAL: string;
	export const COLOR: string;
	export const COLORTERM: string;
	export const _CE_M: string;
	export const npm_config_metrics_registry: string;
	export const OLLAMA_API_BASE: string;
	export const https_proxy: string;
	export const LOGNAME: string;
	export const OLLAMA_PORT: string;
	export const TAURI_FAMILY: string;
	export const _: string;
	export const http_proxy: string;
	export const npm_config_prefix: string;
	export const PKG_CONFIG_PATH: string;
	export const XDG_SESSION_CLASS: string;
	export const JOPLIN_TOKEN: string;
	export const TERM: string;
	export const XDG_SESSION_ID: string;
	export const npm_config_cache: string;
	export const OLLAMA_KEEP_ALIVE: string;
	export const _CE_CONDA: string;
	export const npm_config_node_gyp: string;
	export const PATH: string;
	export const NODE: string;
	export const npm_package_name: string;
	export const XDG_RUNTIME_DIR: string;
	export const SSL_CERT_DIR: string;
	export const STEP_API_KEY: string;
	export const TAURI_PLATFORM: string;
	export const LANG: string;
	export const MACOSX_DEPLOYMENT_TARGET: string;
	export const LS_COLORS: string;
	export const SERVER_PASSWORD: string;
	export const TERM_PROGRAM: string;
	export const VSCODE_GIT_IPC_HANDLE: string;
	export const npm_lifecycle_script: string;
	export const CONDA_PYTHON_EXE: string;
	export const GSETTINGS_SCHEMA_DIR: string;
	export const OLLAMA_MODELS: string;
	export const NLTK_DATA: string;
	export const RUC_ID: string;
	export const SHELL: string;
	export const npm_lifecycle_event: string;
	export const npm_package_version: string;
	export const CONDA_DEFAULT_ENV: string;
	export const LESSCLOSE: string;
	export const VSCODE_GIT_ASKPASS_EXTRA_ARGS: string;
	export const npm_config_globalconfig: string;
	export const npm_config_init_module: string;
	export const CUDA_HOME: string;
	export const PWD: string;
	export const npm_config_globalignorefile: string;
	export const npm_execpath: string;
	export const CONDA_EXE: string;
	export const SSH_CONNECTION: string;
	export const TAURI_TARGET_TRIPLE: string;
	export const npm_config_global_prefix: string;
	export const npm_command: string;
	export const CONDA_PREFIX: string;
	export const GSETTINGS_SCHEMA_DIR_CONDA_BACKUP: string;
	export const EDITOR: string;
	export const INIT_CWD: string;
	export const NODE_ENV: string;
}

/**
 * Similar to [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private), except that it only includes environment variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`), and can therefore safely be exposed to client-side code.
 * 
 * Values are replaced statically at build time.
 * 
 * ```ts
 * import { PUBLIC_BASE_URL } from '$env/static/public';
 * ```
 */
declare module '$env/static/public' {
	
}

/**
 * This module provides access to runtime environment variables, as defined by the platform you're running on. For example if you're using [`adapter-node`](https://github.com/sveltejs/kit/tree/main/packages/adapter-node) (or running [`vite preview`](https://svelte.dev/docs/kit/cli)), this is equivalent to `process.env`. This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured).
 * 
 * This module cannot be imported into client-side code.
 * 
 * Dynamic environment variables cannot be used during prerendering.
 * 
 * ```ts
 * import { env } from '$env/dynamic/private';
 * console.log(env.DEPLOYMENT_SPECIFIC_VARIABLE);
 * ```
 * 
 * > In `dev`, `$env/dynamic` always includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.
 */
declare module '$env/dynamic/private' {
	export const env: {
		LESSOPEN: string;
		CONDA_PROMPT_MODIFIER: string;
		OPENROUTER_API_KEY: string;
		RUC_KEY: string;
		SSH_CLIENT: string;
		USER: string;
		npm_config_user_agent: string;
		GIT_ASKPASS: string;
		XDG_SESSION_TYPE: string;
		npm_node_execpath: string;
		BROWSER: string;
		LD_LIBRARY_PATH: string;
		SHLVL: string;
		TAURI_PLATFORM_VERSION: string;
		npm_config_noproxy: string;
		CONDA_SHLVL: string;
		HOME: string;
		OLDPWD: string;
		TERM_PROGRAM_VERSION: string;
		VSCODE_IPC_HOOK_CLI: string;
		npm_package_json: string;
		TAURI_ARCH: string;
		VSCODE_GIT_ASKPASS_MAIN: string;
		SSL_CERT_FILE: string;
		VSCODE_GIT_ASKPASS_NODE: string;
		npm_config_local_prefix: string;
		npm_config_userconfig: string;
		DBUS_SESSION_BUS_ADDRESS: string;
		TAURI_PLATFORM_TYPE: string;
		VISUAL: string;
		COLOR: string;
		COLORTERM: string;
		_CE_M: string;
		npm_config_metrics_registry: string;
		OLLAMA_API_BASE: string;
		https_proxy: string;
		LOGNAME: string;
		OLLAMA_PORT: string;
		TAURI_FAMILY: string;
		_: string;
		http_proxy: string;
		npm_config_prefix: string;
		PKG_CONFIG_PATH: string;
		XDG_SESSION_CLASS: string;
		JOPLIN_TOKEN: string;
		TERM: string;
		XDG_SESSION_ID: string;
		npm_config_cache: string;
		OLLAMA_KEEP_ALIVE: string;
		_CE_CONDA: string;
		npm_config_node_gyp: string;
		PATH: string;
		NODE: string;
		npm_package_name: string;
		XDG_RUNTIME_DIR: string;
		SSL_CERT_DIR: string;
		STEP_API_KEY: string;
		TAURI_PLATFORM: string;
		LANG: string;
		MACOSX_DEPLOYMENT_TARGET: string;
		LS_COLORS: string;
		SERVER_PASSWORD: string;
		TERM_PROGRAM: string;
		VSCODE_GIT_IPC_HANDLE: string;
		npm_lifecycle_script: string;
		CONDA_PYTHON_EXE: string;
		GSETTINGS_SCHEMA_DIR: string;
		OLLAMA_MODELS: string;
		NLTK_DATA: string;
		RUC_ID: string;
		SHELL: string;
		npm_lifecycle_event: string;
		npm_package_version: string;
		CONDA_DEFAULT_ENV: string;
		LESSCLOSE: string;
		VSCODE_GIT_ASKPASS_EXTRA_ARGS: string;
		npm_config_globalconfig: string;
		npm_config_init_module: string;
		CUDA_HOME: string;
		PWD: string;
		npm_config_globalignorefile: string;
		npm_execpath: string;
		CONDA_EXE: string;
		SSH_CONNECTION: string;
		TAURI_TARGET_TRIPLE: string;
		npm_config_global_prefix: string;
		npm_command: string;
		CONDA_PREFIX: string;
		GSETTINGS_SCHEMA_DIR_CONDA_BACKUP: string;
		EDITOR: string;
		INIT_CWD: string;
		NODE_ENV: string;
		[key: `PUBLIC_${string}`]: undefined;
		[key: `${string}`]: string | undefined;
	}
}

/**
 * Similar to [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private), but only includes variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`), and can therefore safely be exposed to client-side code.
 * 
 * Note that public dynamic environment variables must all be sent from the server to the client, causing larger network requests — when possible, use `$env/static/public` instead.
 * 
 * Dynamic environment variables cannot be used during prerendering.
 * 
 * ```ts
 * import { env } from '$env/dynamic/public';
 * console.log(env.PUBLIC_DEPLOYMENT_SPECIFIC_VARIABLE);
 * ```
 */
declare module '$env/dynamic/public' {
	export const env: {
		[key: `PUBLIC_${string}`]: string | undefined;
	}
}
