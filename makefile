DESTDIR ?= /usr/local/bin

install:
	@sudo cp flagger $(DESTDIR)
	@sudo chmod +x $(DESTDIR)/flagger
	@echo "flagger has been installed"

uninstall:
	@sudo rm -f $(DESTDIR)/flagger
	@echo "flagger has been removed"
