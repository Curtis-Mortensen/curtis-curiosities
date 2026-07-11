# ELI5: This file is the site map. It says which URL opens which page.
# Home, bio, field-notes list, and research report views live here.
# Phase 1 uses stub reports so you can click around before the real
# Research-Bot catalog is wired in phase 2.

Rails.application.routes.draw do
  # Load balancer / uptime check — returns 200 when the app can boot.
  get "up" => "rails/health#show", as: :rails_health_check

  root "home#index"

  get "bio", to: "bios#show", as: :bio
  get "field-notes", to: "field_notes#index", as: :field_notes

  # Shared-chrome report page (nav + iframe into the HTML document).
  get "research/:slug", to: "research#show", as: :research, constraints: { slug: %r{[^/]+} }

  # Bare self-contained HTML for the iframe (and for "open document only").
  get "research/:slug/raw", to: "research#raw", as: :research_raw, constraints: { slug: %r{[^/]+} }
end
