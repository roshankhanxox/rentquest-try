import random
from django.core.management.base import BaseCommand
from faker import Faker
from properties.models import Property, PropertyImage
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "poipulate properties and images in the models"

    def handle(self, *args, **kwargs):
        default_images = [
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843913/2024-01-16_1_r6ldte.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843913/2023-02-08_q3d24j.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843913/2023-05-10_1_ouo8ua.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843913/2023-02-09_viju6c.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843913/2020-10-29_s4fukv.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843912/2024-06-23_szyddt.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843912/2024-01-16_itblyj.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843912/2021-06-15_tgvjoj.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843912/2023-05-10_lq6nxq.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843911/2024-06-23_1_hvytjw.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843911/IMG_20230226_135750_gtpgz6.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843911/img1_dt5xcf.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843911/IMG_2320_jxxddl.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843911/IMG_20210202_164022_umtdgn.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843910/2019-10-17_jndzxn.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843910/WhatsApp_Image_2022-08-05_at_7.15.31_PM_1_sqlne5.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843910/WhatsApp_Image_2022-08-06_at_9.37.27_AM_1_v52ush.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843910/2023-06-10_ay2lnu.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843909/IMG_2267_ryydv3.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843908/IMG_2298_wbhsv0.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843908/2023-11-25_jjux1a.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843908/2022-12-17_hmbsb5.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843908/2024-06-02_1_rntr4o.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843908/IMG_20210202_162945_s7n0oj.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843907/2023-05-09_ckisyd.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843906/2022-11-09_qya2nh.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843905/2022-08-14_uwakcc.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843905/2024-06-02_lq6x0g.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843905/IMG_20221125_181804_zyhaqy.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843905/2024-01-16_2_ungvwn.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843905/2020-10-19_aajbrv.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843905/DSC04774_1024x768_vrmrxe.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843905/DSC_9015_xx63cg.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843904/2022-11-26_numk54.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843904/2021-11-28_zugdcx.jpg",
            "https://res.cloudinary.com/dl7n2c4hr/image/upload/v1728843904/2018-12-18_yjiexh.jpg",
        ]

        # Function to slightly vary the lat/lon
        def randomize_lat_lon(lat, lon):
            lat_variation = random.uniform(
                -0.005, 0.005
            )  # Variation range for latitude
            lon_variation = random.uniform(
                -0.005, 0.005
            )  # Variation range for longitude
            return lat + lat_variation, lon + lon_variation

        # Fake dataset generation
        fake = Faker()
        kolkata_streets = [
            {"name": "Park Street", "lat": 22.552161, "lng": 88.349273},
            {"name": "Gariahat Road", "lat": 22.519824, "lng": 88.366672},
            {"name": "Chowringhee Road", "lat": 22.555248, "lng": 88.353333},
            {"name": "Camac Street", "lat": 22.545553, "lng": 88.353983},
            {"name": "EM Bypass", "lat": 22.542569, "lng": 88.405093},
            {"name": "Southern Avenue", "lat": 22.510023, "lng": 88.357489},
            {"name": "Jadavpur", "lat": 22.498498, "lng": 88.371084},
            {"name": "Ballygunge Place", "lat": 22.526642, "lng": 88.365833},
            {"name": "Prince Anwar Shah Road", "lat": 22.500675, "lng": 88.365812},
            {"name": "Tollygunge Circular Road", "lat": 22.506469, "lng": 88.345438},
            {"name": "Rashbehari Avenue", "lat": 22.522889, "lng": 88.363878},
            {"name": "Salt Lake Sector V", "lat": 22.574776, "lng": 88.429592},
            {"name": "Baguiati", "lat": 22.622144, "lng": 88.434945},
            {"name": "Ultadanga", "lat": 22.599852, "lng": 88.388888},
            {"name": "Kankurgachi", "lat": 22.582495, "lng": 88.392472},
            {"name": "Lake Gardens", "lat": 22.502248, "lng": 88.343839},
            {"name": "Kasba", "lat": 22.522797, "lng": 88.374870},
            {"name": "Behala", "lat": 22.490696, "lng": 88.313904},
            {"name": "Dum Dum", "lat": 22.619992, "lng": 88.392486},
            {"name": "Bhowanipore", "lat": 22.533160, "lng": 88.344132},
            {"name": "Shyambazar", "lat": 22.600841, "lng": 88.377038},
            {"name": "Kalighat", "lat": 22.519401, "lng": 88.344524},
            {"name": "Phoolbagan", "lat": 22.577536, "lng": 88.379628},
            {"name": "Maniktala", "lat": 22.594396, "lng": 88.380876},
            {"name": "Gopalnagar", "lat": 22.538912, "lng": 88.376470},
            {"name": "New Alipore", "lat": 22.513064, "lng": 88.326661},
            {"name": "Jodhpur Park", "lat": 22.508264, "lng": 88.363064},
            {"name": "Dover Lane", "lat": 22.520698, "lng": 88.366737},
            {"name": "Kalindi", "lat": 22.624708, "lng": 88.398312},
            {"name": "Bangur Avenue", "lat": 22.617438, "lng": 88.397198},
            # Streets near Rajarhat/New Town/RR Plot
            {"name": "Rajarhat Main Road", "lat": 22.613230, "lng": 88.464508},
            {"name": "New Town Action Area I", "lat": 22.595768, "lng": 88.466194},
            {"name": "New Town Action Area II", "lat": 22.602987, "lng": 88.481113},
            {"name": "New Town Action Area III", "lat": 22.620928, "lng": 88.499897},
            {"name": "Rajarhat Chinar Park", "lat": 22.620835, "lng": 88.447590},
            {"name": "Unitech Infospace", "lat": 22.579514, "lng": 88.469544},
            {"name": "RR Plot Road", "lat": 22.617450, "lng": 88.470935},
            {"name": "Rajarhat Eco Park Road", "lat": 22.603279, "lng": 88.479362},
            {"name": "Tata Medical Center Road", "lat": 22.604492, "lng": 88.496727},
            {"name": "Street 230, Action Area I", "lat": 22.573342, "lng": 88.465982},
            # Streets near Ruby area
            {"name": "Ruby Connector", "lat": 22.512600, "lng": 88.394480},
            {"name": "Anandapur Road", "lat": 22.514995, "lng": 88.408065},
            {"name": "Kalikapur Road", "lat": 22.508352, "lng": 88.388967},
            {"name": "Mukundapur", "lat": 22.507573, "lng": 88.409451},
            {"name": "Patuli", "lat": 22.475959, "lng": 88.401227},
            # Streets near College Street
            {"name": "College Street", "lat": 22.578110, "lng": 88.364913},
            {"name": "Bidhan Sarani", "lat": 22.586649, "lng": 88.364399},
            {"name": "MG Road", "lat": 22.582548, "lng": 88.357491},
            {"name": "Sovabazar", "lat": 22.596191, "lng": 88.366799},
            {"name": "Amherst Street", "lat": 22.573770, "lng": 88.364624},
        ]
        # Fetch or create a landlord user
        User = get_user_model()
        landlord = User.objects.filter(role="landlord").first()

        if landlord:
            for _ in range(200):  # Adjust the number of properties
                street = random.choice(kolkata_streets)
                lat, lon = randomize_lat_lon(street["lat"], street["lng"])

                # Generate a random building number (e.g., 19, 57)
                building_number = random.randint(1, 100)

                # Construct a distinct address with a building number
                full_address = f"{building_number} {street['name']}"

                # Create the property
                property = Property.objects.create(
                    name=fake.company(),
                    location=full_address,
                    price=random.randint(1000, 25000),
                    size=random.randint(200, 600),
                    landlord=landlord,
                    latitude=lat,
                    longitude=lon,
                )

                # Assign 2-3 random images to each property
                for _ in range(
                    random.randint(2, 3)
                ):  # Ensuring 2-3 images per property
                    PropertyImage.objects.create(
                        property=property,
                        image=random.choice(
                            default_images
                        ),  # Random image from the list
                    )

                print(
                    f"Created property: {property.name} at {full_address}, Lat: {lat}, Lon: {lon}, with 2-3 images"
                )
        else:
            print("No landlord found. Please create a landlord user.")

        # A list of default property images (these are example Cloudinary URLs)
