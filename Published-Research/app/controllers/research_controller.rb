# ELI5: Opens one research HTML report inside the shared site layout.
# show = nav chrome + iframe of the document.
# raw  = the bare self-contained HTML (what the iframe loads).
# Phase 1 uses stub files under sample_reports/; phase 2 will point at Research-Bot/.

class ResearchController < ApplicationController
  def show
    @note = FieldNotes::Catalog.find(params[:slug])
    head :not_found and return unless @note
  end

  def raw
    @note = FieldNotes::Catalog.find(params[:slug])
    head :not_found and return unless @note

    # Send the HTML file as-is — no Rails layout — so Research-Bot-style
    # self-contained documents keep their own CSS.
    send_file @note.html_path, type: "text/html", disposition: "inline"
  end
end
