DESTDIR ?= /usr/local/bin

install:
	@sudo cp ftf $(DESTDIR)
	@sudo chmod +x $(DESTDIR)/ftf
	@echo "Find the Flag has been installed"

uninstall:
	@sudo rm -f $(DESTDIR)/ftf
	@echo "Find the Flag has been removed"
