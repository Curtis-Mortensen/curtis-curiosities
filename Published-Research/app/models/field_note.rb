# ELI5: One "field note" row on the travel site — a title, short teaser,
# and a path to the self-contained HTML report file.
# Controllers and the catalog use this tiny object so pages stay simple.
# Later (phase 2) the catalog will fill these from Research-Bot/*.html;
# phase 1 fills them from sample_reports/ stubs so the site is clickable.

class FieldNote
  attr_reader :slug, :title, :teaser, :html_path

  def initialize(slug:, title:, teaser:, html_path:)
    @slug = slug
    @title = title
    @teaser = teaser
    @html_path = html_path
  end
end
