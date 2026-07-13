# ELI5: Temporary shelf of sample reports so phase 1 is testable without
# scanning Research-Bot yet. Phase 2 will replace these entries with a
# real filesystem scan; keep this file until that swap is done.
# Files live in sample_reports/ at the Rails app root.

module FieldNotes
  class StubCatalog
    # Hard-coded samples — enough to click Home → Field notes → Report.
    SAMPLES = [
      {
        slug: "mesa-dusk-walk",
        title: "Mesa dusk walk",
        teaser: "Sample field note — heat, canal paths, and a sky that turns copper.",
        file: "mesa-dusk-walk.html"
      },
      {
        slug: "harbor-ferry-sketch",
        title: "Harbor ferry sketch",
        teaser: "Sample field note — a short crossing, gulls, and notes for a longer trip log.",
        file: "harbor-ferry-sketch.html"
      }
    ].freeze

    def self.all
      SAMPLES.map { |row| build(row) }
    end

    def self.find(slug)
      row = SAMPLES.find { |sample| sample[:slug] == slug }
      return nil unless row

      build(row)
    end

    def self.build(row)
      FieldNote.new(
        slug: row[:slug],
        title: row[:title],
        teaser: row[:teaser],
        html_path: Rails.root.join("sample_reports", row[:file])
      )
    end
    private_class_method :build
  end
end
