export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["favicon.png","svelte.svg","tauri.svg","vite.svg"]),
	mimeTypes: {".png":"image/png",".svg":"image/svg+xml"},
	_: {
		client: {start:"_app/immutable/entry/start.CKPCgv_m.js",app:"_app/immutable/entry/app.DngeGPVZ.js",imports:["_app/immutable/entry/start.CKPCgv_m.js","_app/immutable/chunks/CanumkPW.js","_app/immutable/chunks/DZcUXPM7.js","_app/immutable/chunks/6yjlgM9W.js","_app/immutable/entry/app.DngeGPVZ.js","_app/immutable/chunks/DZcUXPM7.js","_app/immutable/chunks/CA7uskU_.js","_app/immutable/chunks/8bdQ0ycm.js","_app/immutable/chunks/BD6eZ-V0.js","_app/immutable/chunks/6yjlgM9W.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js'))
		],
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		prerendered_routes: new Set([]),
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();
