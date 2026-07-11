# ELI5: Shows the about / bio page from bio.md.
# Product framing: travel, places lived, mission, IT tech work, Questweight.
# Views: app/views/bios/show.html.erb · Model: BioPage

class BiosController < ApplicationController
  def show
    @bio_text = BioPage.body
  end
end
