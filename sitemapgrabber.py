from usp.tree import sitemap_tree_for_homepage


def getAllURLsForAWebsite(website_url):
    def getURL(siteMapPage):
        return siteMapPage.url;
    return list(map(getURL, sitemap_tree_for_homepage(website_url).all_pages() ))

