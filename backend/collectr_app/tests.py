"""
This files contains all our testcases
"""
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase, client
from django.urls import reverse
from rest_framework import status
from .models import *

class CollectionTestCase(TestCase):
    """
    This class is for testing everything related to collection
    """

    def test_collection_model(self):
        """
        A basic test for collection model
        """
        minecraft = Collection(
            title="Minecraft".title(),
            description="A Mining game (sandbox)",
            cover_image="Minecraft.logo",
            thumbnail="Minecraft.thumbnail"
        )
        # Testing its basic attributes
        self.assertEquals(minecraft.title, "minecraft".title())
        self.assertNotEqual(minecraft.description, "Not minecraft")
        self.assertEquals(minecraft.cover_image, "Minecraft.logo")
        self.assertEquals(minecraft.thumbnail, "Minecraft.thumbnail")
class ItemTestCase(APITestCase):
    """
    This class is for testing everything related to item
    """

    def setUp(self):
        """
        Basic Setup for testing
        """
        self.client = APIClient()
        self.user = Profile.objects.create_user(
            email="real@email.com",
            username="Jo[e]",
            password="apple123!",
            is_active=True
        )
        self.client.force_authenticate(self.user)

        self.collection = Collection.objects.create(title="Food", description="Something Jo[e] likes.")
        self.other_collection = Collection.objects.create(title="Books", description="Something Jo[e] doesn't like.")
        self.breakfast = Item.objects.create(collection=self.collection, name="Porridge")
        self.lunch = Item.objects.create(collection=self.collection, name="Salad")
        self.dinner = Item.objects.create(collection=self.collection, name="Not salad")
        self.JoeHasBreakfast = UserCollectsItem.objects.create(user = self.user, item_id = self.breakfast)

    # viewing collection page (2 x colls shown)
    def test_all_collections(self):
        """
        Basic testing for all collections
        """
        response = self.client.get(reverse("all collections", ))
        # printSpecial(nickname="collections:", value=response.json())
        # printSpecial(nickname="coll 1:", value=response.json()[0]['title'])
        coll1 = response.json()[0]
        coll2 = response.json()[1]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(coll1['title'], "Books")
        self.assertEqual(coll1['item_count'], 0)
        self.assertEqual(coll2['title'], "Food")
        self.assertEqual(coll2['item_count'], 3)


    # viewing item detail page
    #     response = self.client.get(reverse("api-one-trade", kwargs={"pk": trade.id}))
    def test_item_detail(self):
        """
        Testing Item detail
        """
        item_id = self.lunch.id
        response = self.client.get(reverse("item detail", kwargs={"item_id": item_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item0 = response.json()['name']
        self.assertEqual(item0, "Salad")

    # # collecting items into my own collection

    # def test_my_collections(self):
    #     user_id = str(self.user.id)
    #     item_id = str(self.breakfast.id)
    #     printSpecial(nickname="user", value=user_id)
    #     printSpecial(nickname="item", value=item_id)
    #     response = self.client.post(reverse("collect more",  kwargs={"user_id": user_id, "item_id": item_id}))
    #     printSpecial(nickname="response_dump:", value=response.json())


    # viewing my collection only (1 x coll shown)
    def test_my_collections(self):
        """
        Testing my own collection
        """
        response = self.client.get(reverse("all my collections", ))
        coll1 = response.json()[0]
        coll2 = None
        try:
            coll2 = response.json()[1]
        except IndexError:
            pass
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(coll2, None)  # Jo[e] is indifferent to books.
        self.assertEqual(coll1['title'], "Food")  # Jo[e] has breakfast.
        self.assertEqual(coll1['item_count'], 3)

    # viewing single collection
    def test_single_collections(self):
        """
        Testing a single collection of sets of collections
        """
        food_id = self.collection.id
        response = self.client.get(reverse("single collection", kwargs={"collection_id": food_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        coll_name = response.json()['results']['Collection'][0]['title']
        self.assertEqual(coll_name, "Food")

        item0 = response.json()['results']['Item'][0]['name']
        self.assertEqual(item0, "Not salad")

        item1 = response.json()['results']['Item'][1]['name']
        self.assertEqual(item1, "Porridge")

        item2 = response.json()['results']['Item'][2]['name']
        self.assertEqual(item2, "Salad")

        item4 = None
        try:
            response.json()['results']['Item'][3]
        except IndexError:
            pass
        self.assertEqual(item4, None)  # no more food.


    # viewing my items within single collection
    def test_my_single_collections(self):
        """
        Testing a single personal collection
        """
        food_id = self.collection.id
        response = self.client.get(reverse("my single collection", kwargs={"collection_id": food_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        coll_name = response.json()[0]['collection']
        self.assertEqual(coll_name, str(food_id))

        item0 = response.json()[0]['name']
        self.assertEqual(item0, "Porridge")

        item1 = None
        try:
            response.json()[1]['name']
        except IndexError:
            pass
        self.assertEqual(item1, None)  # Jo[e] has no more food at this time.

class NewCollectionRequestTestCase(TestCase):
    """
    A class for testing everything related to NewCollectionRequest
    """

    def setUp(self):
        """
        Setting up attributes for testing
        """
        self.client = APIClient()
        self.requester = Profile.objects.create_user(
            email="noreply@collectr.com",
            username="Kirito",
            password="TheElucidatorXXX",
            is_active=True
        )
        self.client.force_authenticate(self.requester)

    def test_requesting_new_collection(self):
        """
        A test method for testing basic request
        """
        minecraft_request = NewCollectionRequest(
            requester = self.requester,
            new_name="Minecraft",
            description="Sandbox game made by Jeff and Notch",
            evidence="Horses",
            isActive=True,
            isApproved=False
        )
        # Test Section
        self.assertIs(minecraft_request.requester, self.requester)
        self.assertTrue(minecraft_request.isActive)
        self.assertFalse(minecraft_request.isApproved)
        self.assertEquals(minecraft_request.new_name, "Minecraft")
        self.assertNotEqual(minecraft_request.description, "Hey")

    def test_request_new_collection_in_DB(self):
        """
        Adding a new collection request to the database
        """
        new_request = NewCollectionRequest.objects.create(
            requester=self.requester,
            new_name="Dota 2".title(),
            description="A different kind of moba game",
            evidence="The Toxicity",
            isActive=True,
            isApproved=False
        )
        # Test Section
        request_id = new_request.id
        self.assertEquals(new_request, NewCollectionRequest.objects.get(id=request_id))

        # Changing the attributes of request
        new_request.isApproved = True
        new_request.new_name="League of Legend"
        new_request.description="A fast paced Moba game"
        new_request.isActive= False
        new_request.save()
        self.assertTrue(NewCollectionRequest.objects.get(id=request_id).isApproved)
        self.assertFalse(NewCollectionRequest.objects.get(id=request_id).isActive)
        self.assertEquals(NewCollectionRequest.objects.get(id=request_id).new_name,
                          "League of Legend")
        self.assertNotEquals(NewCollectionRequest.objects.get(id=request_id).description,
                             "Dota 2 is better")

    def test_request_removal(self):
        """
        A method for testing request removal
        """
        new_request = NewCollectionRequest.objects.create(
            requester = self.requester,
            new_name="Super Smash Ultimate",
            description="DLC",
            evidence="Link, Fire Emblems, ...",
            isActive=True,
            isApproved=False
        )
        # Test comparison
        request_id = new_request.id
        self.assertEquals(new_request, NewCollectionRequest.objects.get(id=request_id))

        # Removal Testing
        new_request.delete()
        self.assertNotIn(new_request, NewCollectionRequest.objects.all())

    def test_add_approve_remove(self):
        """
        A complex test cases for new collection request
        """
        # Adding:
        new_request = NewCollectionRequest.objects.create(
            requester=self.requester,
            new_name="The Legend of Runeterra",
            description="A very exciting card game",
            evidence="Bandle City",
            isActive=True,
            isApproved=False
        )

        # Testing request creations
        request_id = new_request.id
        self.assertEquals(new_request, NewCollectionRequest.objects.get(id=request_id))
        self.assertTrue(NewCollectionRequest.objects.get(id=request_id).isActive)
        self.assertFalse(NewCollectionRequest.objects.get(id=request_id).isApproved)

        # Approving the request
        new_request.isApproved = True
        new_request.isActive = False
        new_request.save()
        self.assertTrue(NewCollectionRequest.objects.get(id=request_id).isApproved)
        self.assertFalse(NewCollectionRequest.objects.get(id=request_id).isActive)

        # Removing the approved request
        new_request.delete()
        self.assertNotIn(new_request, NewCollectionRequest.objects.all())

    def test_add_deny_remove(self):
        """
        A complex test cases for new collection request
        """
        # Adding:
        new_request = NewCollectionRequest.objects.create(
            requester=self.requester,
            new_name="Candy Crush",
            description="A very exciting card game",
            evidence="Candy in the name",
            isActive=True,
            isApproved=False
        )

        # Testing request creations
        request_id = new_request.id
        self.assertEquals(new_request, NewCollectionRequest.objects.get(id=request_id))
        self.assertTrue(NewCollectionRequest.objects.get(id=request_id).isActive)
        self.assertFalse(NewCollectionRequest.objects.get(id=request_id).isApproved)

        # Approving the request
        new_request.isApproved = False
        new_request.isActive = False
        new_request.save()
        self.assertFalse(NewCollectionRequest.objects.get(id=request_id).isApproved)
        self.assertFalse(NewCollectionRequest.objects.get(id=request_id).isActive)

        # Removing the approved request
        new_request.delete()
        self.assertNotIn(new_request, NewCollectionRequest.objects.all())

class NewItemRequestTestCase(TestCase):
    """
    This class contains all the testcases related to new item request
    """

    def setUp(self):
        """
        A basic set up for the testcases
        """
        self.client = APIClient()
        self.requester = Profile.objects.create_user(
            email="violet@hotmail.com",
            username="Vi stands for Violence",
            password="Cupcake",
            is_active="True"
        )
        self.client.force_authenticate(self.requester)
        self.pokemon = Collection.objects.create(
            title="Pokemon",
            description="A massive collection of epic monsters",
            cover_image="Pokemon.png",
            thumbnail="Pokemon_tn.png"
        )

    def test_new_item_request_model(self) -> None:
        """
        A testcase for new item request model
        """
        snorlax = NewItemRequest(
            requester=self.requester,
            add_to_collection=self.pokemon,
            new_name="Snorlax",
            description="A normal type pokemon",
            evidence="A big chubby boi",
            isActive=True,
            isApproved=False
        )
        self.assertEquals(snorlax.requester, self.requester)
        self.assertEquals(snorlax.add_to_collection, self.pokemon)
        self.assertEquals(snorlax.new_name, "Snorlax")
        self.assertEquals(snorlax.description, "A normal type pokemon")
        self.assertIsNotNone(snorlax.evidence)
        self.assertTrue(snorlax.isActive)
        self.assertFalse(snorlax.isApproved)

    def test_new_item_request_in_DB(self) -> None:
        """
        A testcase for request in the database
        """
        new_request = NewItemRequest.objects.create(
            requester=self.requester,
            add_to_collection=self.pokemon,
            new_name="Magikarp",
            description="Only know splash",
            evidence="Red Gyrados",
            isActive=True,
            isApproved=False
        )
        request_id = new_request.id
        self.assertEquals(new_request, NewItemRequest.objects.get(id=request_id))

        # Changing the attributes of request
        new_request.isApproved = True
        new_request.new_name="Gyrados"
        new_request.description="magikarp evolution"
        new_request.isActive= False
        new_request.save()
        self.assertTrue(NewItemRequest.objects.get(id=request_id).isApproved)
        self.assertFalse(NewItemRequest.objects.get(id=request_id).isActive)
        self.assertEquals(NewItemRequest.objects.get(id=request_id).new_name,
                          "Gyrados")
        self.assertNotEquals(NewItemRequest.objects.get(id=request_id).description,
                             "Bidoof")

    def test_removal_request(self) -> None:
        """
        A testcase for removing request
        """
        new_request = NewItemRequest.objects.create(
            requester = self.requester,
            new_name = "Palkia",
            description = "The god of space",
            evidence = "Pokemon Pearl",
            add_to_collection = self.pokemon,
            isActive = True,
            isApproved = False
        )

        # Testing the existence
        request_id = new_request.id
        self.assertEquals(new_request, NewItemRequest.objects.get(id=request_id))

        # Test removal
        new_request.delete()
        self.assertNotIn(new_request, NewItemRequest.objects.all())

    def test_add_approve_remove(self) -> None:
        """
        A complex test for adding, approving then remove the request
        """
        new_request = NewItemRequest.objects.create(
            requester = self.requester,
            new_name = "Dialga",
            description = "The god of time",
            evidence = "Pokemon Diamond",
            add_to_collection = self.pokemon,
            isActive = True,
            isApproved = False
        )

        # Testing the existence
        request_id = new_request.id
        self.assertEquals(new_request, NewItemRequest.objects.get(id=request_id))

        new_request.isActive = False
        new_request.isApproved = True
        new_request.save()
        self.assertFalse(NewItemRequest.objects.get(id=request_id).isActive)
        self.assertTrue(NewItemRequest.objects.get(id=request_id).isApproved)

        # Removing the request
        new_request.delete()
        self.assertNotIn(new_request, NewItemRequest.objects.all())

    def test_add_deny_remove(self) -> None:
        """
        A complex test for adding, denying then remove the request
        """
        new_request = NewItemRequest.objects.create(
            requester = self.requester,
            new_name = "Dialga",
            description = "The god of time",
            evidence = "Pokemon Diamond",
            add_to_collection = self.pokemon,
            isActive = True,
            isApproved = False
        )

        # Testing the existence
        request_id = new_request.id
        self.assertEquals(new_request, NewItemRequest.objects.get(id=request_id))

        new_request.isActive = False
        new_request.isApproved = False
        new_request.save()
        self.assertFalse(NewItemRequest.objects.get(id=request_id).isActive)
        self.assertFalse(NewItemRequest.objects.get(id=request_id).isApproved)

        # Removing the request
        new_request.delete()
        self.assertNotIn(new_request, NewItemRequest.objects.all())

class TradeFunctionalityTests(TestCase):
    """
    Defines all the test cases around trade-related functionality
    """

    def setUp(self):
        self.client = APIClient()
        self.user = Profile.objects.create_user(email="test@gmail.com", username="test", password="apple123!", is_active=True)
        self.client.force_authenticate(self.user)

        self.trader_1 = Profile.objects.create(email="foo@gmail.com", username="foo")
        self.trader_2 = Profile.objects.create(email="bar@gmail.com", username="bar")
        self.collection_tf2 = Collection.objects.create(title="Team Fortress 2", description="War-themed hat simulator")
        self.festive_flamethrower = Item.objects.create(collection=self.collection_tf2, name="Festive Flamethrower")
        self.gunslinger = Item.objects.create(collection=self.collection_tf2, name="Gunslinger")
        self.eyelander = Item.objects.create(collection=self.collection_tf2, name="Eyelander")

    def test_get_all_trades(self):
        trade1 = Trade.objects.create(creator=self.trader_1, description="This is a test trade!")
        trade1.have.add(self.gunslinger)
        trade1.want.add(self.eyelander)
        trade2 = Trade.objects.create(creator=self.trader_2, description="This is another test trade!")
        trade2.have.add(self.festive_flamethrower)
        trade2.want.add(self.gunslinger)

        response = self.client.get(reverse("api-all-trades"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        trade1_data = response.data[1]
        self.assertEqual(trade1_data['id'], str(trade1.id))
        self.assertEqual(trade1_data['creator']['id'], str(self.trader_1.id))
        self.assertEqual(trade1_data['description'], trade1.description)
        self.assertEqual(trade1_data['have'][0]['id'], str(self.gunslinger.id))
        self.assertEqual(trade1_data['want'][0]['id'], str(self.eyelander.id))

        trade2_data = response.data[0]
        self.assertEqual(trade2_data['id'], str(trade2.id))
        self.assertEqual(trade2_data['creator']['id'], str(self.trader_2.id))
        self.assertEqual(trade2_data['description'], trade2.description)
        self.assertEqual(trade2_data['have'][0]['id'], str(self.festive_flamethrower.id))
        self.assertEqual(trade2_data['want'][0]['id'], str(self.gunslinger.id))

    def test_get_single_trade(self):
        trade = Trade.objects.create(creator=self.trader_1, description="This is a test trade!")

        trade.have.add(self.festive_flamethrower)
        trade.want.add(self.gunslinger)

        # items
        self.assertIn(self.festive_flamethrower, trade.have.all())
        self.assertIn(self.gunslinger, trade.want.all())

        # other details
        self.assertEqual("This is a test trade!", trade.description)
        self.assertTrue(trade.active)
        self.assertEqual(self.trader_1, trade.creator)
        self.assertEqual(0, len(trade.attachments.all()))
        self.assertEqual(0, len(trade.bookmarks.all()))
        self.assertEqual(0, len(trade.comments.all()))

        response = self.client.get(reverse("api-one-trade", kwargs={"pk":trade.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(trade.id))
        self.assertEqual(response.data['description'], trade.description)
        self.assertEqual(response.data['creator']['id'], str(trade.creator.id))
        self.assertEqual(response.data['have'][0]['id'], str(self.festive_flamethrower.id))
        self.assertEqual(response.data['want'][0]['id'], str(self.gunslinger.id))

    def test_trade_search(self):

        trade = Trade.objects.create(creator=self.trader_1, description="This is a test trade!")
        trade.have.add(self.festive_flamethrower)
        trade.want.add(self.gunslinger)
        trade2 = Trade.objects.create(creator=self.trader_1, description="Sale!")
        trade2.have.add(self.eyelander)
        trade2.want.add(self.gunslinger)

        response = self.client.get("%s?description=test" % reverse("api-all-trades"))
        self.assertEqual(response.data[0]['id'], str(trade.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get("%s?description=sale" % reverse("api-all-trades"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], str(trade2.id))

        get_param = "%s?have=" + str(self.festive_flamethrower.id)
        response = self.client.get(get_param % reverse("api-all-trades"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], str(trade.id))

        get_param = "%s?have=" + str(self.eyelander.id)
        response = self.client.get(get_param % reverse("api-all-trades"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], str(trade2.id))

        get_param = "%s?want=" + str(self.gunslinger.id)
        response = self.client.get(get_param % reverse("api-all-trades"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], str(trade.id))
        self.assertEqual(response.data[1]['id'], str(trade2.id))

        get_param = "%s?want=" + str(self.festive_flamethrower.id) + "&have=" + str(self.eyelander.id)
        response = self.client.get(get_param % reverse("api-all-trades"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], str(trade2.id))

    def test_toggle_bookmark(self):
        trade = Trade.objects.create(creator=self.trader_1, description="This is a test trade!")
        self.assertEqual(0, len(Trade.objects.filter(bookmarks=self.user)))

        response = self.client.post(reverse("api-bookmark-toggle", kwargs={"trade_id":str(trade.id)}), format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(Trade.objects.filter(bookmarks=self.user)))

        response = self.client.post(reverse("api-bookmark-toggle", kwargs={"trade_id": str(trade.id)}), format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, len(Trade.objects.filter(bookmarks=self.user)))

    def test_get_user_trades_and_bookmarks(self):

        trade1 = Trade.objects.create(creator=self.user, description="This is a test trade! (1)")
        trade2 = Trade.objects.create(creator=self.user, description="This is a test trade! (2)")
        self.assertEqual(2, len(Trade.objects.filter(creator=self.user)))

        response = self.client.get(reverse("api-user-trades", kwargs={"user_id":str(self.user.id)}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        trade1_data = response.data[0]
        self.assertEqual(trade1_data['id'], str(trade2.id))
        self.assertEqual(trade1_data['creator']['id'], str(self.user.id))
        self.assertEqual(trade1_data['description'], trade2.description)
        trade2_data = response.data[1]
        self.assertEqual(trade2_data['id'], str(trade1.id))
        self.assertEqual(trade2_data['creator']['id'], str(self.user.id))
        self.assertEqual(trade2_data['description'], trade1.description)

        trade2.bookmarks.add(self.user)
        response = self.client.get(reverse("api-user-bookmarks", kwargs={"user_id": self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.data[0]
        self.assertEqual(response['id'], str(trade2.id))
        self.assertEqual(response['creator']['id'], str(self.user.id))
        self.assertEqual(response['description'], trade2.description)
        self.assertEqual(1, len(Trade.objects.filter(bookmarks=self.user)))

    def test_bookmarks_multiple_user_interaction(self):

        trade = Trade.objects.create(creator=self.trader_1, description="This is a test trade!")
        self.assertEqual(0, len(trade.bookmarks.all()))
        trade.bookmarks.add(self.trader_1)
        trade.bookmarks.add(self.trader_2)
        self.assertIn(self.trader_1, trade.bookmarks.all())
        self.assertIn(self.trader_2, trade.bookmarks.all())
        self.assertEqual(2, len(trade.bookmarks.all()))
        trade.bookmarks.remove(self.trader_1)
        self.assertNotIn(self.trader_1, trade.bookmarks.all())
        self.assertIn(self.trader_2, trade.bookmarks.all())
        self.assertEqual(1, len(trade.bookmarks.all()))
        trade.bookmarks.remove(self.trader_2)
        self.assertNotIn(self.trader_2, trade.bookmarks.all())
        self.assertEqual(0, len(trade.bookmarks.all()))

    def test_create_and_close_trades(self):

        # trade create

        trade_data = {
            "creator":str(self.user.id),
            "description":"Sending a trade now!",
            "active":True,
            "have":str(self.eyelander.id),
            "want":str(self.festive_flamethrower.id)
        }

        self.assertEqual(0, len(Trade.objects.all()))
        response = self.client.post(reverse("api-create-trade"), trade_data, format="multipart")
        trade_id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, len(Trade.objects.all()))

        response = self.client.get(reverse("api-one-trade", kwargs={"pk":trade_id}), trade_data, format="multipart")
        trade = Trade.objects.get(id=trade_id)
        self.assertEqual(response.data['id'], str(trade.id))
        self.assertEqual(response.data['creator']['id'], str(trade.creator.id))
        self.assertEqual(response.data['have'][0]['id'], str(self.eyelander.id))
        self.assertEqual(response.data['want'][0]['id'], str(self.festive_flamethrower.id))
        self.assertEqual(response.data['active'], True)

        # trade close
        update_data = {
            "active":False
        }
        response = self.client.patch(reverse("api-one-trade", kwargs={"pk":trade_id}), update_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        trade = Trade.objects.get(id=trade_id)
        self.assertFalse(trade.active)
        response = self.client.get(reverse("api-one-trade", kwargs={"pk":trade_id}), trade_data, format="multipart")
        self.assertEqual(response.data['active'], False)

    def test_comment_interactions(self):

        trade = Trade.objects.create(creator=self.user, description="This is a test trade!")
        self.assertEqual(0, len(trade.comments.all()))

        comment_data = {
            "trade":str(trade.id),
            "username":str(self.user.username),
            "email":str(self.user.email),
            "comment":"Item for sale!"
        }

        response = self.client.post(reverse("api-one-trade-comments", kwargs={"pk":trade.id}), comment_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, len(trade.comments.all()))

        comment_data = {
            "trade":str(trade.id),
            "username":str(self.trader_1.username),
            "email":str(self.trader_1.email),
            "comment":"Can I get a discount?"
        }

        response = self.client.post(reverse("api-one-trade-comments", kwargs={"pk":trade.id}),
                                    comment_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, len(trade.comments.all()))

        comment_data = {
            "trade":str(trade.id),
            "username":str(self.trader_2.username),
            "email":str(self.trader_2.email),
            "comment":"Statutory misleading and deceptive conduct pursuant to s 18 of the ACL (Cth)!"
        }

        response = self.client.post(reverse("api-one-trade-comments", kwargs={"pk":trade.id}),
                                    comment_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, len(trade.comments.all()))

        response = self.client.get(reverse("api-one-trade-comments", kwargs={"pk":trade.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["comment"], "Item for sale!")
        self.assertEqual(response.data[1]["comment"], "Can I get a discount?")
        self.assertEqual(response.data[2]["comment"], "Statutory misleading and deceptive conduct pursuant to s 18 of the ACL (Cth)!")
