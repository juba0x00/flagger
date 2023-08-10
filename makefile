DESTDIR ?= /usr/local/bin

install:
	@sudo cp rorensics $(DESTDIR)
	@sudo chmod +x $(DESTDIR)/rorensics
	@echo "Find the Flag has been installed"

uninstall:
	@sudo rm -f $(DESTDIR)/rorensics
	@echo "Find the Flag has been removed"
