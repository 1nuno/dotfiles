return {
	"neovim/nvim-lspconfig",
	-- opts = {
	-- 	capabilities = {
	-- 		textDocument = {
	-- 			foldingRange = {
	-- 				dynamicRegistration = false,
	-- 				lineFoldingOnly = true,
	-- 			},
	-- 		},
	-- 	},
	-- },
	config = function()
		local capabilities = require("cmp_nvim_lsp").default_capabilities() -- this is to enable completion to use our lsp
		local lspconfig = require("lspconfig")
		lspconfig.clangd.setup({
			capabilities = capabilities, -- this is to enable completion to use our lsp
		})
		lspconfig.pyright.setup({
			capabilities = capabilities, -- this is to enable completion to use our lsp
		})
		lspconfig.lua_ls.setup({
			capabilities = capabilities, -- this is to enable completion to use our lsp
			settings = {
				Lua = {
					diagnostics = {
						-- Get the language server to recognize the `vim` global
						globals = { "vim", "opts" },
					},
				},
			},
		})
		vim.keymap.set("n", "K", vim.lsp.buf.hover, {})
		vim.keymap.set("n", "gd", vim.lsp.buf.definition, opts)
		vim.keymap.set({ "n", "v" }, "<space>a", vim.lsp.buf.code_action, opts)
	end,
}
