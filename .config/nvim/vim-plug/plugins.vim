" auto-install vim-plug
if empty(glob('~/.config/nvim/autoload/plug.vim'))
  silent !curl -fLo ~/.config/nvim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  "autocmd VimEnter * PlugInstall
  "autocmd VimEnter * PlugInstall | source $MYVIMRC
endif

call plug#begin('~/.config/nvim/autoload/plugged')

    " Better Syntax Support
    Plug 'sheerun/vim-polyglot'
    " File Explorer
    Plug 'scrooloose/NERDTree'
    " Auto pairs for '(' '[' '{'
    Plug 'jiangmiao/auto-pairs'
    " onedark theme
    Plug 'joshdick/onedark.vim'    
    " Stable version of coc
    Plug 'neoclide/coc.nvim', {'branch': 'release'}
    " airline status line 
    Plug 'vim-airline/vim-airline'
    Plug 'vim-airline/vim-airline-themes'
    " for ranger terminal file manager
    Plug 'kevinhwang91/rnvimr', {'do': 'make sync'}
    " add colour to hex and rgb values 
    Plug 'norcalli/nvim-colorizer.lua'
    " add rainbox extension to colour parentheses
    Plug 'junegunn/rainbow_parentheses.vim'
    " FZF and rooter
    Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
    Plug 'junegunn/fzf.vim'
    Plug 'airblade/vim-rooter'
    " vim key reminder
    Plug 'liuchengxu/vim-which-key'
    " for commenting lines 
    Plug 'tpope/vim-commentary'
    " sneak command to move through file
    Plug 'justinmk/vim-sneak'
    " git plugins 
    Plug 'mhinz/vim-signify'
    Plug 'tpope/vim-fugitive'
    Plug 'tpope/vim-rhubarb'
    Plug 'junegunn/gv.vim'
    " open a floating terminal (+ other programs) from neovim
    Plug 'voldikss/vim-floaterm'
call plug#end()

