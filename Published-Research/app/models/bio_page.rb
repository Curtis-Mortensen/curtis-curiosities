# ELI5: Reads the human-written bio.md file and hands the text to the
# bio page. Keeps the voice in one markdown file (not buried in a view)
# so Curtis can edit the story without touching Rails templates.

class BioPage
  PATH = Rails.root.join("bio.md")

  def self.body
    PATH.read
  end
end
