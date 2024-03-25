return {

	{
		"hrsh7th/cmp-nvim-lsp",
	},

	{
		"L3MON4D3/LuaSnip",
		dependencies = {
			"saadparwaiz1/cmp_luasnip",
			"rafamadriz/friendly-snippets",
		},
	},

	{
		"hrsh7th/nvim-cmp",
		config = function()
			local cmp = require("cmp")
			require("luasnip.loaders.from_vscode").lazy_load()

			cmp.setup({
				snippet = {
					expand = function(args)
						require("luasnip").lsp_expand(args.body)
					end,
				},
				window = {
					completion = cmp.config.window.bordered(),
					documentation = cmp.config.window.bordered(),
				},

				mapping = cmp.mapping.preset.insert({
					["<C-j>"] = cmp.mapping.select_next_item({ behavior = cmp.SelectBehavior.Select }),
					["<C-k>"] = cmp.mapping.select_prev_item({ behavior = cmp.SelectBehavior.Select }),
					["<C-u>"] = cmp.mapping.scroll_docs(-4),
					["<C-d>"] = cmp.mapping.scroll_docs(4),
					["<C-s>"] = cmp.mapping.complete(), --> this is for showing the completion in case its closed
					["<C-w>"] = cmp.mapping.abort(), --> this is for closing the completion
					["<Tab>"] = cmp.mapping.confirm({ select = true }),
				}),
				sources = cmp.config.sources({
					{ name = "nvim_lsp" },
					{ name = "luasnip" }, -- For luasnip users.
				}, {
					{ name = "buffer" },
				}),
			})
		end,
	},

	{ "williamboman/mason.nvim", opts = {} },

	{
		"williamboman/mason-lspconfig.nvim",
		opts = {
			ensure_installed = { "lua_ls", "clangd", "pyright", "tsserver" },
		},
	},

	{
		"neovim/nvim-lspconfig",
		config = function()
			local capabilities = require("cmp_nvim_lsp").default_capabilities() -- this is to enable completion to use our lsp
			local lspconfig = require("lspconfig")

			lspconfig.clangd.setup({
				capabilities = capabilities,
				filetypes = { "c", "cpp", "objc", "objcpp" }, -- for C, C++, Objective-C, and Objective-C++
			})
			lspconfig.emmet_language_server.setup({
				capabilities = capabilities,
				filetypes = { "javascriptreact", "typescriptreact" }, -- for JS and TS
			})

			lspconfig.bashls.setup({
				capabilities = capabilities,
				filetypes = { "sh", "bash" }, -- for shell scripts
			})

			lspconfig.tsserver.setup({
				capabilities = capabilities,
				filetypes = { "javascript", "javascriptreact", "typescript", "typescriptreact" }, -- for JS and TS
			})

			lspconfig.pyright.setup({
				capabilities = capabilities,
				filetypes = { "python" }, -- for Python files
			})

			lspconfig.lua_ls.setup({
				capabilities = capabilities,
				settings = {
					Lua = {
						diagnostics = {
							globals = { "vim", "opts" },
						},
					},
				},
				filetypes = { "lua" }, -- for Lua files
			})

			lspconfig.taplo.setup({ capabilities = capabilities })
			lspconfig.marksman.setup({ capabilities = capabilities })
			vim.keymap.set("n", "K", vim.lsp.buf.hover, {})
			vim.keymap.set("n", "gd", vim.lsp.buf.definition, opts)
			vim.keymap.set({ "n", "v" }, "<space>a", vim.lsp.buf.code_action, opts)
		end,
	},

	{
		"stevearc/conform.nvim",
		event = { "BufReadPre", "BufNewFile" },
		config = function()
			local conform = require("conform")
			conform.setup({
				formatters_by_ft = {
					lua = { "stylua" },
					python = { "black" },
					c = { "clang_format" },
					javascript = { "prettierd" },
				},
			})

			vim.keymap.set({ "n", "v" }, "<leader>f", function()
				conform.format({
					lsp_fallback = true,
					async = false,
					timeout_ms = 500,
				})
			end, { desc = "Format file or range (in visual mode)" })
		end,
	},

	{
		"nvim-neo-tree/neo-tree.nvim",
		branch = "v3.x",
		dependencies = {
			"nvim-lua/plenary.nvim",
			"nvim-tree/nvim-web-devicons",
			"MunifTanjim/nui.nvim",
		},
		config = function()
			vim.keymap.set("n", "<C-n>", ":Neotree toggle<CR>", {})
			vim.keymap.set("n", "<Leader>n", ":Neotree focus<CR>", {})
		end,
	},
}
