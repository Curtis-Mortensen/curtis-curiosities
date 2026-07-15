# ELI5: The librarian for field notes. Controllers ask this object
# "list everything" or "find this slug" — they do not care whether the
# answers come from stub samples (phase 1) or Research-Bot files (phase 2).
# Sibling: FieldNotes::StubCatalog holds the temporary sample data.

module FieldNotes
  class Catalog
    # Every note the site should show on /field-notes.
    def self.all
      StubCatalog.all
    end

    # One note by URL slug, or nil if nobody matches.
    def self.find(slug)
      StubCatalog.find(slug)
    end
  end
end
