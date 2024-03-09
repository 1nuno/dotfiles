return {
    "AckslD/swenv.nvim",
    config = function()
        local swenv = require("swenv")
        swenv.setup({
            get_venvs = function(venvs_path)
                return require('swenv.api').get_venvs(venvs_path)
            end,

            venvs_path = vim.fn.expand('~/Desktop/virtual_envs'),

            post_set_venv = function()
               vim.cmd("LspRestart")
            end
    })

    -- vim.keymap.set({ "n", "v" }, "<leader>f", function()
    --     swenv.format({
    --         lsp_fallback = true,
    --         async = false,
    --         timeout_ms = 500,
    --     })
    -- end,
    -- { desc = "Format file or range (in visual mode)" })
end,
}
-- return {
-- 		"stevearc/swenv.nvim", --> github page mentioned above.
-- 		event = { "BufReadPre", "BufNewFile" },
-- 		config = function()
-- 			local swenv = require("swenv")
-- 			swenv.setup({
-- 				formatters_by_ft = { -- table mentioned above
-- 					lua = { "stylua" },
-- 					python = { "black" },
-- 					c = { "clang_format" },
-- 				},
-- 			})
--
-- 			vim.keymap.set({ "n", "v" }, "<leader>f", function()
-- 				swenv.format({
-- 					lsp_fallback = true,
-- 					async = false,
-- 					timeout_ms = 500,
-- 				})
-- 			end, { desc = "Format file or range (in visual mode)" })
-- 		end,
-- 	}
