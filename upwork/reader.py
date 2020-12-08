from upwork.models import Profile
from upwork.tag_map import UpWorkTagkMap
from upwork.utils import smart_split, letters_only, get_value
from bs4 import BeautifulSoup


class UpWorkReader:

    def __init__(self):
        self.contact = {}
        self.profile = {
            "employments": [],
            "others": [],
            "education": []
        }
        self.tags = UpWorkTagkMap()

    def get_full_profile(self) -> Profile:
        """
        Function that returns a Profile pydantic model
        :return:
        """
        return Profile(**{**self.profile, **self.contact})

    def get_profile(self, html_content: str) -> object:
        """
        Read the profile page and update the class self.profile object
        :param html_content:
        :return:
        """
        if not html_content:
            raise Exception("HTML content not found")

        soup = BeautifulSoup(html_content, 'html.parser')

        self.profile = {
            "employments": [],
            "others": [],
            "education": []
        }
        # get sidebar
        sidebar = soup.select_one(self.tags.get("sidebar"))
        items = sidebar.select(self.tags.get("sidebar.items")) if sidebar else []

        # read each item on sidebar
        for item in items:

            label = item.select_one(self.tags.get("sidebar.items.header"))
            section_title = label.text.strip()

            # Availability Item
            if section_title == 'Availability':
                status, avaibility = smart_split(
                    get_value(item.select_one(self.tags.get("sidebar.items.availability"))), '\n')
                self.profile["status"] = status
                self.profile["avaibility"] = avaibility

            # Languages Item
            elif section_title == 'Languages':

                languages = [' '.join(get_value(li).split()) for li in
                             item.select(self.tags.get("sidebar.items.languages.item"))]
                self.profile["languages"] = [dict(zip(["name", "level"], lng.split(":"))) for lng in languages]

            # Education Item
            elif section_title == 'Education':
                lis = item.select(self.tags.get("sidebar.items.education.item"))

                for li in lis:
                    school = " ".join(
                        get_value(li.select_one(self.tags.get("sidebar.items.education.school"))).split())
                    degree_area = get_value(li.select_one(self.tags.get("sidebar.items.education.degree_area")))
                    degree, area = smart_split(degree_area)
                    attended_date = get_value(li.select_one(self.tags.get("sidebar.items.education.attended_date")))

                    self.profile["education"].append({
                        "school": school,
                        "degree": degree,
                        "area": area,
                        "attended_date": attended_date
                    })

        # Skill panel
        skills = soup.select(self.tags.get("skills"))
        self.profile["skills"] = set(get_value(s) for s in skills)  # using set to remove duplications

        # Employment/Other Experience panels
        cards = soup.select(self.tags.get("profile.panels"))
        for lis in cards:
            lis = lis.parent.select("li")

            for li in lis:
                position, employer = smart_split(
                    li.select_one(self.tags.get("employments.position_employer")).get_text(strip=True), "|")
                period = ' '.join(li.select_one(self.tags.get("employments.period")).get_text(strip=True).split())

                if "Other" != position.strip():
                    self.profile["employments"].append({
                        "employer": employer,
                        "job_title": position,
                        "hire_datetime": period.split('-')[0].strip(),
                        "termination_datetime": period.split('-')[1].strip()
                    })
                else:
                    self.profile["others"].append({
                        "title": employer,
                        "description": period.split('-')[0]
                    })

        title = soup.select_one(self.tags.get("title"))
        hour = get_value(title.parent.parent.select_one(self.tags.get("hour_price")))
        description = get_value(soup.select_one(self.tags.get("description")))

        # define the last elements of profile
        self.profile["title"] = get_value(title)
        self.profile["price"] = hour
        self.profile["description"] = description
        self.profile["full_name"] = soup.select_one(self.tags.get("full_name")).get_text(strip=True)
        self.profile["first_name"] = self.profile["full_name"].split()[0]
        self.profile["last_name"] = self.profile["full_name"].split()[-1]
        self.profile["address_city"] = soup.select_one(self.tags.get("address_city")).get_text(strip=True)
        self.profile["address_country"] = soup.select_one(self.tags.get("address_country")).get_text(strip=True)
        self.profile["picture_url"] = soup.select_one(self.tags.get("picture"))["src"]

        return self.profile

    def get_contact_info(self, html_content: str) -> object:
        """
        Read the contact page and update the class self.contact object
        :param html_content:
        :return:
        """
        if not html_content:
            raise Exception("HTML content not found")

        soup = BeautifulSoup(html_content, 'html.parser')

        self.contact = {}
        cards = soup.select(self.tags.get("contact.panels"))

        # read cards panels for cotnact info
        for card in cards:
            form = card.parent.select_one("form")

            # if is form of user information
            if form:
                rows = form.select(self.tags.get("contact.form.row"))
                for row in rows:
                    label = row.select_one(self.tags.get("contact.form.row.label")).get_text(strip=True)
                    value = row.select_one(self.tags.get("contact.form.row.value")).get_text(strip=True)

                    if label == "User ID":
                        self.contact["account"] = value

                    elif label == "Name":
                        self.contact["full_name"] = value

                    elif label == "Email":
                        self.contact["email"] = value

            else:
                lis = card.parent.select("li")
                for li in lis:
                    label = li.select_one("label").get_text(strip=True)
                    if label == "Address":
                        street1 = get_value(li.select_one(self.tags.get("contact.address.street1"))).strip()
                        street2 = get_value(li.select_one(self.tags.get("contact.address.street2"))).strip()
                        state = get_value(li.select_one(self.tags.get("contact.address.state"))).strip()
                        postalcode = get_value(li.select_one(self.tags.get("contact.address.zip"))).strip()

                        self.contact["address_line1"] = street1
                        self.contact["address_line2"] = street2
                        self.contact["address_state"] = letters_only(state.strip())
                        self.contact["address_postal_code"] = postalcode

                    elif label in ["Phone", "Time Zone"]:

                        key = "phone_number" if label == "Phone" else "timezone"
                        self.contact[key] = li.select_one(self.tags.get("contact.phone")).get_text(strip=True).strip()

        return self.contact
