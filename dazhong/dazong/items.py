# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class memberItem(Item):
    # define the fields for your item here like:
    # name = Field()
    consumer_name = Field()
    record_data = Field()
    lastlogon = Field()
    empirical = Field()
    contribution = Field()
    location = Field()
    label = Field()  # use ''.join(label)  sometime is empty
    gender = Field()
    pass

class fansItem(Item):
    consumer_name = Field()  #use the same name
    fans_name = Field()
    fans_http = Field()    
    pass

class followsItem(Item):
    consumer_name = Field()  #use the same name
    follows_name = Field()
    follows_http = Field()    
    pass

class reviewsItem(Item):
    consumer_name = Field()  #use the same name
    shop_name = Field()
    shop_http = Field() 
    shop_location = Field()
    #shop_grade = Field() 
    #shop_taste = Field()
    #shop_environment = Field() 
    #shop_serve = Field()
    #shop_price = Field()
    reviews_data = Field()
    shop_reviews = Field()    
    pass

class checkinItem(Item):
    consumer_name = Field() #use the same name
    checkin_time = Field()
    checkin_shop = Field() 
    checkin_location = Field()
    #checkin_grade = Field() 
    #checkin_reviews = Field()    
    pass

class wishlistsItem(Item):
    consumer_name = Field() #use the same name
    wishlists_name = Field()
    wishlists_http = Field() 
    wishlists_location = Field()
    wishlists_data = Field()
    pass


class shopItem(Item):
    good_name = Field() 
    good_price = Field()
    good_estimate = Field()
    good_address = Field()
    telephone = Field()
    classification_name = Field()
    classes = Field()
    comment = Field()
    data = Field()
    pass






