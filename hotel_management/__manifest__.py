{
    'name' : 'Hotel Management system',
    'summary': """App to manage Hotel releated Services""",
    'author' : 'Krish',
    'description' : 'Hotel Management System',
    "version": "18.0",
    'depends' : ['base','account','mail'],
    'sequence' : 1,
    'application' : True,
    'license' : 'LGPL-3',


    'data' : [
       'security/ir.model.access.csv',
       'data/room_category_data.xml',
       'data/email_template.xml',
       'data/ir_sequence.xml',
       'views/hotel_reservation_view.xml',
       'views/hotel_guest_view.xml',
       'views/hotel_room_view.xml',
       'views/hotel_room_category_view.xml',
    ],
}