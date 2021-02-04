CC=riscv64-unknown-elf-gcc
CXXFILT=riscv64-unknown-elf-c++filt
SDIR=data/main.c
FILE=main.c
CFLAGS= -O0
ABI=
ARCH=
DUMP_AST=-fdump-tree-original-raw
DUMP_GIMPLE_FLAG=-fdump-tree-gimple-raw
DUMP_GIMPLE_LOWER_FLAG=-fdump-tree-lower
DUMP_CFG=-fdump-tree-cfg
DUMP_SSA=-fdump-tree-ssa 
DUMP_RTL_FLAG=-da
DUMP_ASSEMBLY=-S
# -fdump-tree-optimized it's the last pass before going into rtl passes
DUMP_ALL_TREE=-dump-tree-all

all: assembly lower-gimple high-gimple cfg

assembly:
	@$(CC) $(CFLAGS) $(ABI) $(ARCH) $(DUMP_ASSEMBLY) $(FILE) -o $(SDIR)/tmp.s
	@cat $(SDIR)/tmp.s | $(CXXFILT) -_ | grep -vE '\s+\.[^l]' > $(SDIR)/assembly.s
	@rm $(SDIR)/tmp.s
high-gimple:
	@$(CC) $(CFLAGS) $(ABI) $(ARCH) $(DUMP_ASSEMBLY) $(DUMP_GIMPLE_FLAG) $(FILE) -o $(SDIR)/_.s
	@mv $(SDIR)/$(FILE)*.gimple $(SDIR)/$(FILE).gimple
lower-gimple:
	@$(CC) $(CFLAGS) $(ABI) $(ARCH)$(DUMP_ASSEMBLY) $(DUMP_GIMPLE_LOWER_FLAG) $(FILE) -o $(SDIR)/_.s
	@cat $(SDIR)/$(FILE)*.lower | $(CXXFILT) > $(SDIR)/tmp.res
	@rm $(SDIR)/$(FILE)*.lower
	@mv $(SDIR)/tmp.res $(SDIR)/$(FILE).gimple.lower 
cfg:
	@$(CC) $(CFLAGS) $(ABI) $(ARCH) $(DUMP_ASSEMBLY) $(DUMP_CFG) $(FILE) -o $(SDIR)/_.s
	@mv $(SDIR)/$(FILE)*.cfg $(SDIR)/$(FILE).cfg
ssa:
	@$(CC) $(CFLAGS) $(ABI) $(ARCH) $(DUMP_ASSEMBLY) $(DUMP_SSA) $(FILE) -o $(SDIR)/_.s
	@mv $(SDIR)/$(FILE)*.ssa $(SDIR)/$(FILE).ssa
app:
	@rm -rf $(SDIR)
	@mkdir -p $(SDIR)/rtl
	@$(CC) $(CFLAGS) $(ABI) $(ARCH) $(DUMP_ASSEMBLY) $(DUMP_GIMPLE_FLAG) $(DUMP_CFG) $(DUMP_SSA) $(DUMP_GIMPLE_LOWER_FLAG) $(FILE) -o $(SDIR)/tmp.s
	@cat $(SDIR)/tmp.s | $(CXXFILT) -_ | grep -vE '\s+\.[^l]' > $(SDIR)/assembly.s
	@rm $(SDIR)/tmp.s
	@mv $(SDIR)/$(FILE)*.cfg $(SDIR)/$(FILE).cfg
	@mv $(SDIR)/$(FILE)*.ssa $(SDIR)/$(FILE).ssa
	@cat $(SDIR)/$(FILE)*.lower | $(CXXFILT) > $(SDIR)/tmp.res
	@rm $(SDIR)/$(FILE)*.lower
	@mv $(SDIR)/tmp.res $(SDIR)/$(FILE).gimple.lower
	@mv $(SDIR)/$(FILE)*.gimple $(SDIR)/$(FILE).gimple
	@$(CC) $(CFLAGS) $(ABI) $(ARCH) $(DUMP_ASSEMBLY) $(DUMP_RTL_FLAG) $(FILE) -o $(SDIR)/rtl/tmp.s
	@rm $(SDIR)/rtl/tmp.s