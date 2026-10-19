/**
 * Browser bookmarklet: fetch Mobalytics tier list JSON while logged into the site.
 *
 * Usage:
 * 1. Open https://mobalytics.gg/slay-the-spire-2/tier-lists/cards
 * 2. Run this script from the console (or save as a bookmarklet).
 * 3. Save the downloaded tier-lists-raw.json to Scrape-Ventures/STS2/
 * 4. Run: python tier-list/scrape/fetch-tier-lists.py --raw
 */
(async () => {
  const query = `query Sts2TierLists($input: Sts2UserGeneratedDocumentInputBySlug!) {
    game: sts2 {
      documents {
        userGeneratedDocumentBySlug(input: $input) {
          error
          data {
            data {
              tierLists {
                values {
                  id
                  tierSections {
                    name
                    staticDataItems { name slug iconUrl linkUrl type }
                  }
                  staticDataSources { slug tags { slug groupSlug } }
                }
              }
            }
            content {
              __typename
              ... on NgfDocumentCmWidgetTierListMakerV1 { id data { title } }
            }
          }
        }
      }
    }
  }`;

  const response = await fetch("/api/sts2/v1/graphql/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      operationName: "Sts2TierLists",
      variables: { input: { slug: "cards", type: "tier-lists" } },
      query,
    }),
  });

  const json = await response.json();
  const blob = new Blob([JSON.stringify(json, null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "tier-lists-raw.json";
  link.click();
  console.log("Downloaded tier-lists-raw.json", json);
})();
