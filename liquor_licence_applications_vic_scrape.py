from liquor_licence_applications_vic import LiquorLicenceApplicationsVic


webpuppet = LiquorLicenceApplicationsVic()
webpuppet.get_browser()
# webpuppet.scrape()
webpuppet.get_lgas()
print(webpuppet.lga_names)

# webpuppet.export_data()
