-- to add a new formater just add a new entry to the table << formatters_by_ft >> down below. (dont forget to make sure that you have the desired formater installed by mason. for more info checkout the github page for this plugin or the help page.
return {
		"stevearc/conform.nvim", --> github page mentioned above.
		event = { "BufReadPre", "BufNewFile" },
		config = function()
			local conform = require("conform")
			conform.setup({
				formatters_by_ft = { -- table mentioned above
					lua = { "stylua" },
					python = { "black" },
					c = { "clang_format" },
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
	}
