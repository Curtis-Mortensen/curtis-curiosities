# ELI5: Lists research reports as "field notes" teasers in site chrome.
# Phase 1 pulls stub samples so you can test the list → report path.
# Views: app/views/field_notes/index.html.erb · Catalog: FieldNotes::Catalog

class FieldNotesController < ApplicationController
  def index
    @notes = FieldNotes::Catalog.all
  end
end
