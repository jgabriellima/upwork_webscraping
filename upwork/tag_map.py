
class UpWorkTagkMap:

    def __init__(self, tags_map=None):
        self.__map = {
            "title": "h2[role='presentation']",
            "full_name": "h1[itemprop='name']",
            "address_city": "span[itemprop='locality']",
            "address_country": "span[itemprop='country-name']",
            "picture": "div[class^='cfe-ui-profile-photo'] img",
            "hour_price": "h3[role='presentation']",
            "description": "div.up-line-clamp-origin span[class^='text-pre-line']",
            "sidebar": "aside[class^='up-sidebar']",
            "sidebar.items": "div[class='mt-30']",
            "sidebar.items.header": "h4[role='presentation']",
            "sidebar.items.availability": "p",
            "sidebar.items.languages.item": "li",
            "sidebar.items.education.item": "li",
            "sidebar.items.education.school": "h5[role='presentation']",
            "sidebar.items.education.degree_area": ":nth-child(2)",
            "sidebar.items.education.attended_date": ":nth-child(3)",
            "skills": "div[class='skills'] span[class='up-skill-badge']",
            "employments.position_employer": "h4[role='presentation']",
            "employments.period": ":nth-child(2)",
            "profile.panels": "div[class^='up-card'] header",
            "profile.panels.item": "li",
            "contact.panels": "div[class^='air-card'] header",
            "contact.form.row": "div[class^='row']",
            "contact.form.row.label": ":nth-child(1) label",
            "contact.form.row.value": ":nth-child(2)",
            "contact.address.street1": "div[ng-if='vm.address.street']",
            "contact.address.street2": "div[ng-if='vm.address.additionalInfo']",
            "contact.address.city": "div[ng-if='vm.address.city']",
            "contact.address.state": "span[ng-if='vm.address.state']",
            "contact.address.zip": "span[ng-if='vm.address.zip']",
            "contact.phone": ":nth-child(2)"
        }
        if tags_map:
            self.__map.update(tags_map)

    def get(self, key):
        return self.__map.get(key)

