"""Editorial content and brand directory for the Dante Media staging website.

All relationships, operating claims, launch statuses and links should be approved
by the group before publishing. Do not add a brand just because it appears in a
partner pitch, and never equate partner distribution with owned operations.
"""

SITE_NAME = 'Dante Media'
SITE_URL = 'https://www.dante-media.io'
GROUP_EMAIL = ''  # IMPORTANT: Populate with a verified official group email before going live.

BRANDS = [
    dict(name='PlayBeSpoke', category='gaming', label='Gaming & Technology', status='Platform / active development', description='Bespoke game creation and a multi-studio production ecosystem, built for operators, studios and creators.', url='https://playbespoke.com', icon='PB', accent='gold', note='Flagship platform'),
    dict(name='Hustle Labs', category='gaming', label='Game Studios', status='Studio', description='Original gaming experiences and new formats developed within the wider Dante Media ecosystem.', url='', icon='HL', accent='blue', note='Studio'),
    dict(name='Lucky Bastards', category='gaming', label='Game Studios', status='Studio', description='A distinctive game studio developing character-led gaming experiences.', url='', icon='LB', accent='lilac', note='Studio'),
    dict(name="Dante’s Games", category='gaming', label='Game Studios', status='Studio', description='Original games with a creative identity and a focus on entertainment.', url='', icon='DG', accent='gold', note='Studio'),
    dict(name='Mad Games', category='gaming', label='Game Studios', status='Studio', description='Part of our wider network of game-development ventures and collaborations.', url='', icon='MG', accent='rose', note='Studio'),
    dict(name='Boludo Games', category='gaming', label='Game Studios', status='Collaborative studio', description='A studio collaboration contributing original game concepts and production capability.', url='', icon='BG', accent='mint', note='Studio collaboration'),
    dict(name='KOIVOLT Games', category='gaming', label='Game Studios', status='Brand in development', description='An Asia-oriented gaming studio identity in development.', url='', icon='KV', accent='blue', note='Developing'),
    dict(name='IGW³', category='media', label='Media & Intelligence', status='Preparing for launch', description='An intelligence, news and discovery destination built around the iGaming and Web3 sectors.', url='https://igamingandweb3.com', icon='IG', accent='lilac', note='Industry intelligence'),
    dict(name='The Plug TV', category='media', label='Media & Entertainment', status='In development', description='A music, entertainment and community-content concept designed to connect artists with audiences and opportunities.', url='', icon='TV', accent='rose', note='Entertainment'),
    dict(name='Futpal', category='sport', label='Sport & Community', status='Platform in development', description='Connecting grassroots football: people, clubs, leagues, associations and local communities.', url='https://futpal.io', icon='FP', accent='mint', note='Grassroots football'),
    dict(name='The Plug Bet', category='entertainment', label='Entertainment & Ventures', status='Concept / development', description='A proposed entertainment-led gaming venture within the wider Plug ecosystem.', url='', icon='TP', accent='rose', note='Future venture'),
    dict(name='Broken Homes', category='impact', label='Foundation / Social Impact', status='Foundation planned', description='Our shared commitment to expanding access to support, mentorship and opportunity for young people and families facing difficult circumstances.', url='/broken-homes/', icon='BH', accent='gold', note='At the heart of the group'),
]

NAV = [
    ('Our businesses','/businesses/'),
    ('Our approach','/approach/'),
    ('Broken Homes','/broken-homes/'),
    ('Partnerships','/partnerships/'),
    ('About','/about/'),
]

PAGE_META = {
    '/': ('Dante Media | Building businesses. Opening doors.', 'Dante Media brings together gaming, technology, media, sport and entertainment ventures around a shared commitment to create real opportunity.'),
    '/businesses/': ('Our Businesses | Dante Media', 'Explore the ventures, studios and initiatives connected to Dante Media across technology, gaming, media, entertainment, sport and social impact.'),
    '/approach/': ('Our Approach | Dante Media', 'How Dante Media develops ambitious ventures through independent brands, shared expertise and a commitment to social impact.'),
    '/gaming/': ('Gaming & Technology | Dante Media', 'Discover our gaming ecosystem, including PlayBeSpoke and a growing network of creative studios and collaborations.'),
    '/media/': ('Media & Entertainment | Dante Media', 'Discover our media, intelligence, storytelling and entertainment ventures.'),
    '/sport/': ('Sport & Community | Dante Media', 'Futpal and the role of sport in creating connection, opportunity and stronger communities.'),
    '/broken-homes/': ('Broken Homes | The Heart of Dante Media', 'Broken Homes is the social-impact foundation Dante Media plans to launch, connecting people with mentorship, community support and new opportunities.'),
    '/partnerships/': ('Partnerships | Dante Media', 'Partner with Dante Media across technology, content, distribution, grassroots sport or community impact.'),
    '/work/': ('Our Work | Dante Media', 'Explore selected ventures and initiatives taking shape across the Dante Media ecosystem.'),
    '/about/': ('About Us | Dante Media', 'Learn about the ambition, principles and people-first mission behind the Dante Media ecosystem.'),
    '/news/': ('News & Updates | Dante Media', 'Follow the latest official announcements from Dante Media and its ventures.'),
    '/contact/': ('Contact | Dante Media', 'Find the right route for enquiries about Dante Media, its businesses and the upcoming Broken Homes foundation.'),
}
