from faker import Faker
import random
from reviews.models import Review
from properties.models import Property
from api.models import User
from django.utils import timezone
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populate reviews for properties"

    def handle(self, *args, **kwargs):
        # Your code to populate reviews
        fake = Faker()

        positive_templates = [
            "I absolutely loved staying here! The {property_size} property was well-maintained and located in a {location} neighborhood. The landlord was very {landlord_behavior}, making the entire process smooth. Highly recommend this place!",
            "This was one of the best rental experiences I've had. The {property_size} property was exactly as described, and the location in {location} was perfect for my needs. The landlord was {landlord_behavior}.",
            "Such a fantastic place! The {location} neighborhood is great, and the property is {property_condition}. The landlord was always {landlord_behavior}. Would definitely stay again!",
            "What a wonderful experience! The {property_size} property exceeded my expectations, and the {location} area was vibrant and welcoming. The landlord was incredibly {landlord_behavior}.",
            "This rental was perfect for my stay! The {property_size} property had all the amenities I needed, and the location in {location} was fantastic. The landlord was {landlord_behavior} throughout my visit.",
            "I couldn't have asked for a better place to stay! The {location} area was lively, and the {property_size} property was spotless. The landlord was very {landlord_behavior}, ensuring everything went smoothly.",
            "Fantastic experience overall! The {property_size} property was in a great location in {location}, and the landlord was exceptionally {landlord_behavior}. I would love to come back!",
            "The property was lovely and well-kept! I appreciated the {property_size} layout and how convenient it was to {location}. The landlord was very {landlord_behavior} during my stay.",
            "I was pleasantly surprised by how great this property was! The {location} area is beautiful, and the {property_size} property was very {property_condition}. The landlord was {landlord_behavior} as well.",
            "This place was a gem! The {property_size} property had everything I needed, and the {location} was perfect for exploring. The landlord was super {landlord_behavior} and helpful.",
            "I had an amazing time! The {property_size} property in {location} was exactly what I was looking for, and the landlord's {landlord_behavior} made my stay even better.",
            "What a great rental! The {property_size} property was very spacious and located in a quiet {location}. The landlord was {landlord_behavior} and attentive to my needs.",
            "Such a delightful stay! The {location} neighborhood was charming, and the {property_size} property was well-maintained. The landlord was very {landlord_behavior}.",
            "Absolutely stunning property! The {property_size} size was perfect, and the {location} area offered plenty to explore. The landlord was incredibly {landlord_behavior}.",
            "I highly recommend this place! The {property_size} property was comfortable, and the {location} was convenient. The landlord was very {landlord_behavior} during my stay.",
            "The best rental experience I've had! The {property_size} property was in pristine condition, and the {location} neighborhood was delightful. The landlord was {landlord_behavior}.",
            "This property is a must-stay! The {property_size} property was just what I needed, and the {location} area had so much to offer. The landlord was very {landlord_behavior}.",
            "Loved my time here! The {property_size} property was cozy, and the {location} neighborhood was perfect. The landlord was very {landlord_behavior} and helpful.",
            "Fantastic location! The {property_size} property was spacious and comfortable. The landlord was incredibly {landlord_behavior}, making my stay enjoyable.",
            "What a lovely stay! The {location} area was beautiful, and the {property_size} property was well-appointed. The landlord was very {landlord_behavior}.",
            "I couldn't ask for a better experience! The {property_size} property was lovely, and the {location} offered everything I needed. The landlord was exceptionally {landlord_behavior}.",
            "This rental exceeded my expectations! The {property_size} property was beautiful, and the {location} neighborhood was lively. The landlord was very {landlord_behavior}.",
            "I had a wonderful stay! The {property_size} property was perfect for my needs, and the {location} was fantastic. The landlord was very {landlord_behavior}.",
            "The perfect rental! The {property_size} property was very clean, and the {location} neighborhood was enjoyable. The landlord was {landlord_behavior} and accommodating.",
            "Great experience overall! The {property_size} property was well-kept, and the {location} area had a lot to offer. The landlord was very {landlord_behavior}.",
            "This property is highly recommended! The {property_size} size was perfect, and the {location} was convenient for my plans. The landlord was very {landlord_behavior} throughout.",
            "I enjoyed every moment of my stay! The {property_size} property was fantastic, and the {location} neighborhood was delightful. The landlord was incredibly {landlord_behavior}.",
            "Amazing place to stay! The {property_size} property was exactly what I needed, and the {location} was vibrant. The landlord was very {landlord_behavior} and helpful.",
            "I had such a pleasant experience here! The {property_size} property was spacious and the {location} neighborhood was lovely. The landlord was very {landlord_behavior} throughout.",
        ]

        neutral_templates = [
            "The property was decent, though I think the {property_size} size could have been a bit bigger. The location in {location} was okay, but a little far from the main attractions. The landlord was {landlord_behavior}.",
            "It was a good stay, nothing too special but also no major complaints. The {location} neighborhood was fine, and the property was in {property_condition} condition. Overall, an average experience.",
            "The property itself was decent, though I had some issues with {property_problem}. The location in {location} is alright, and the landlord was {landlord_behavior}. Not bad, but also not the best.",
            "My stay was acceptable, but the {property_size} property was not as described. The location in {location} had its pros and cons. The landlord was {landlord_behavior}, but not very responsive.",
            "It was an average rental experience. The {location} area was decent, but the {property_size} property could use some upgrades. The landlord was {landlord_behavior}, but I expected more.",
            "The {property_size} property was okay, but the {location} neighborhood didn’t have much to offer. The landlord was {landlord_behavior} but didn’t go above and beyond.",
            "Decent property overall. The {property_size} size was fine for my needs, but I expected a bit more from the {location}. The landlord was {landlord_behavior}, which was helpful.",
            "Not a bad experience, but the {property_condition} property left some room for improvement. The {location} was nice, but not as lively as I hoped. The landlord was {landlord_behavior}.",
            "The property was satisfactory but could use some improvements. The {location} neighborhood was average, and the landlord was {landlord_behavior}. Overall, it met my needs.",
            "My stay was fine, though the {property_size} property didn’t wow me. The {location} area was pleasant, but the landlord was only {landlord_behavior}.",
            "I had a decent experience here. The {property_size} property was acceptable, but the {location} didn’t have as much to do as I expected. The landlord was {landlord_behavior}.",
            "It was a reasonable rental, but I felt the {property_condition} property didn’t fully match its description. The {location} neighborhood was fine. The landlord was {landlord_behavior}.",
            "My stay was average. The {property_size} property was just okay, and the {location} area didn’t offer much excitement. The landlord was {landlord_behavior} but not very engaging.",
            "The property was alright, but I think it could have been cleaner. The {location} neighborhood was satisfactory, and the landlord was {landlord_behavior}. Not a bad option overall.",
            "The {property_size} property was decent, but the {location} area didn’t have a lot of amenities. The landlord was {landlord_behavior}, which made things easier.",
            "It was a reasonable place to stay. The {property_size} property had its ups and downs, and the {location} was just fine. The landlord was {landlord_behavior}, which was a plus.",
            "I had a fair stay, but the {property_condition} property didn’t meet all my expectations. The {location} was passable. The landlord was {landlord_behavior} but could be better.",
            "It was an okay experience, but the {property_size} property didn’t stand out. The {location} area was fine, but the landlord was {landlord_behavior} without much engagement.",
            "The stay was tolerable, but the {property_size} property had some issues. The {location} was acceptable, and the landlord was {landlord_behavior} throughout.",
            "It was a decent rental overall. The {property_size} property was acceptable, and the {location} neighborhood was just okay. The landlord was {landlord_behavior}, but I expected more.",
            "My experience was satisfactory, though the {property_condition} property could have been better. The {location} was not bad. The landlord was {landlord_behavior}, which was appreciated.",
            "The property was acceptable, but I felt it could use some updates. The {location} area was fine, but the landlord was only {landlord_behavior}. Not terrible, but not great either.",
            "The stay was average. The {property_size} property was decent, and the {location} had some good points, but overall it was just okay. The landlord was {landlord_behavior}.",
            "My time here was fine, but the {property_condition} property could have been improved. The {location} neighborhood was acceptable, and the landlord was {landlord_behavior}.",
        ]

        negative_templates = [
            "I had a pretty bad experience. The {property_size} property felt cramped, and the location in {location} was {location_problem}. The landlord was {landlord_behavior}, which made things worse.",
            "The property was in {property_condition} condition, and the neighborhood of {location} was {location_problem}. Would not recommend staying here. The landlord was {landlord_behavior}, which added to the issues.",
            "This was not a great experience. The {property_size} size was disappointing, and the {location} neighborhood had {location_problem}. The landlord was {landlord_behavior}. I wouldn't stay here again.",
            "I was very disappointed with my stay. The {property_size} property had several issues, and the {location} area was {location_problem}. The landlord's {landlord_behavior} didn’t help matters.",
            "My experience was below expectations. The {property_size} property was poorly maintained, and the {location} neighborhood felt unsafe. The landlord was {landlord_behavior}, which was frustrating.",
            "The property was not worth the price. The {property_size} size was inadequate, and the {location} was {location_problem}. The landlord was {landlord_behavior}, making things worse.",
            "I wouldn't recommend this place. The {property_size} property had multiple problems, and the {location} was not ideal. The landlord was {landlord_behavior} and unhelpful.",
            "The stay was disappointing. The {property_size} property was not as described, and the {location} area was {location_problem}. The landlord's {landlord_behavior} only added to the frustration.",
            "This rental was a letdown. The {property_size} property felt neglected, and the {location} neighborhood had a lot of issues. The landlord was {landlord_behavior}, which didn’t help.",
            "I regretted my stay here. The {property_size} property had major flaws, and the {location} was very {location_problem}. The landlord was {landlord_behavior} and unresponsive.",
            "The experience was poor overall. The {property_size} property was not clean, and the {location} area was {location_problem}. The landlord was {landlord_behavior}, which made it worse.",
            "Not a good rental experience. The {property_size} property was cramped, and the {location} neighborhood left a lot to be desired. The landlord was {landlord_behavior} and not helpful.",
            "I had significant issues during my stay. The {property_size} property was uncomfortable, and the {location} was very {location_problem}. The landlord's {landlord_behavior} didn’t resolve anything.",
            "I do not recommend this property. The {property_size} property was in terrible shape, and the {location} neighborhood was {location_problem}. The landlord was {landlord_behavior} and dismissive.",
            "The stay was frustrating. The {property_size} property was poorly equipped, and the {location} was disappointing. The landlord's {landlord_behavior} added to the problems.",
            "I had a really bad experience here. The {property_size} property didn’t meet my needs, and the {location} was {location_problem}. The landlord was {landlord_behavior}, making it worse.",
            "Not worth the money spent. The {property_size} property was unkempt, and the {location} area had a lot of issues. The landlord was {landlord_behavior} and uncooperative.",
            "This rental fell short. The {property_size} property had a lot of problems, and the {location} was {location_problem}. The landlord was {landlord_behavior}, which didn’t help at all.",
            "I won't be returning. The {property_size} property was disappointing, and the {location} neighborhood had many {location_problem}. The landlord's {landlord_behavior} made things worse.",
            "My stay was not enjoyable. The {property_size} property was too small, and the {location} area was {location_problem}. The landlord was {landlord_behavior}, adding to the frustration.",
            "The rental was subpar. The {property_size} property was neglected, and the {location} neighborhood was quite {location_problem}. The landlord was {landlord_behavior} and unhelpful.",
            "I had a regrettable experience. The {property_size} property didn’t meet my expectations, and the {location} was {location_problem}. The landlord's {landlord_behavior} was disappointing.",
        ]

        # Define some behaviors, property conditions, problems, etc.
        landlord_behaviors = [
            "very responsive",
            "not helpful at all",
            "kind but slow to respond",
            "very professional",
        ]
        property_conditions = ["excellent", "good", "decent", "poor"]
        property_sizes = ["spacious", "cramped", "just right"]
        location_problems = [
            "far from public transport",
            "noisy",
            "a bit unsafe",
            "too crowded",
        ]
        property_problems = [
            "the plumbing",
            "the heating system",
            "the internet connection",
            "the kitchen appliances",
        ]

        def generate_review_text(property):
            # Randomly select a template and fill in the placeholders
            template_type = random.choice(["positive", "neutral", "negative"])
            if template_type == "positive":
                template = random.choice(positive_templates)
            elif template_type == "neutral":
                template = random.choice(neutral_templates)
            else:
                template = random.choice(negative_templates)

            # Fill in template placeholders
            review_text = template.format(
                property_size=random.choice(property_sizes),
                location=property.location,
                landlord_behavior=random.choice(landlord_behaviors),
                property_condition=random.choice(property_conditions),
                location_problem=random.choice(location_problems),
                property_problem=random.choice(property_problems),
            )

            return review_text

        def populate_realistic_reviews():
            properties = Property.objects.all()
            users = User.objects.filter(
                role="student"
            )  # Assuming students leave reviews

            for property in properties:
                for _ in range(random.randint(7, 20)):  # 15-20 reviews per property
                    review = Review(
                        property=property,
                        user=random.choice(users),  # Assign review to a random user
                        rating=random.randint(1, 5),  # Random rating between 1-5
                        comment=generate_review_text(
                            property
                        ),  # Generate realistic review
                        created_at=fake.date_time_between(
                            start_date="-1y", end_date=timezone.now()
                        ),
                    )
                    review.save()
                print(f"reviews populated for property: {property.id}")

            print("Realistic reviews populated successfully!")

        # Call this function to populate reviews
        populate_realistic_reviews()
