DESTDIR ?= /usr/local/bin

install:
	@sudo cp flagger $(DESTDIR)
	@sudo chmod +x $(DESTDIR)/flagger

uninstall:
	@sudo rm -f $(DESTDIR)/flagger
	@echo "flagger has been removed"
