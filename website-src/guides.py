"""Guides: long-form answers that rank and get cited by AI assistants. Each entry renders to /guides/<slug>."""

GUIDES = [
    dict(
        slug='whatsapp-automation-for-business',
        tag='AI Automation',
        title='WhatsApp Automation for Business in India: A Practical Guide',
        h1='WhatsApp automation for business',
        desc='How WhatsApp automation works for Indian businesses: the Business app vs the Business Platform, what to automate, the rules to follow and how to set it up.',
        read='7 min read',
        answer='WhatsApp automation means letting software send and answer WhatsApp messages for your business: instant replies to common questions, booking flows, order updates and timed follow-ups, with a person taking over when needed. Small setups can start on the free WhatsApp Business app; higher volumes and smart flows need the WhatsApp Business Platform through an approved provider.',
        sections=[
            ('Why businesses in India automate WhatsApp', [
                'For most Indian customers WhatsApp is the default way to contact a business. That is great for reach and hard on small teams: the same ten questions arrive all day, enquiries come in after hours, and a lead that waits too long simply messages a competitor.',
                'Automation fixes the repetitive part. Customers get an answer in seconds, every enquiry is logged, and your team only steps in for the conversations that need a person.']),
            ('WhatsApp Business app or WhatsApp Business Platform?', [
                '<strong>The WhatsApp Business app</strong> is free and runs on a phone. It offers a greeting message, an away message, quick replies, labels and a catalogue. It suits a single owner handling a modest number of chats.',
                '<strong>The WhatsApp Business Platform</strong> (often called the WhatsApp API) is for businesses that need several team members on one number, chatbot flows, CRM connections or messages at scale. It is accessed through Meta directly or an approved provider, and business-started messages use templates that Meta reviews.',
                'A simple rule: if one person can comfortably answer every chat, start with the app. If messages are piling up or you want flows and a CRM, move to the Platform.']),
            ('What you can automate', [
                '<ul><li><strong>Common questions:</strong> prices, timings, location, delivery areas and policies.</li><li><strong>Catalogue and enquiries:</strong> share products or services and capture what the customer wants.</li><li><strong>Bookings:</strong> appointments, table reservations, demo classes and site visits, with reminders.</li><li><strong>Order and status updates:</strong> confirmations, dispatch and delivery messages.</li><li><strong>Lead qualification:</strong> two or three questions such as budget, area and timeline, then a tag for your team.</li><li><strong>Follow-ups:</strong> a reminder to customers who asked for a quote and went quiet.</li></ul>']),
            ('The rules to follow', [
                'WhatsApp is strict about spam, and following the rules protects your number:',
                '<ul><li>Message people only after they have opted in to hear from you.</li><li>When a customer messages you, you can reply freely within the customer service window (24 hours from their last message). Outside it, the Platform only allows approved template messages.</li><li>Meta charges for template messages by category, such as marketing, utility and authentication. Check Meta\'s current rate card for India before planning broadcasts.</li><li>Keep a clear way to reach a human, and honour requests to stop messages.</li></ul>']),
            ('How to set it up in five steps', [
                '<ol><li><strong>List the questions</strong> you answer every day and the steps from first message to sale.</li><li><strong>Choose the app or the Platform</strong> based on volume and team size.</li><li><strong>Write the replies</strong> in your brand voice, short and specific, with a human handover for anything unusual.</li><li><strong>Connect your tools:</strong> a CRM or a Google Sheet so every lead is saved, and your own WhatsApp for alerts on hot leads.</li><li><strong>Test, launch and review monthly:</strong> read real conversations, add answers and improve what converts.</li></ol>']),
            ('Mistakes to avoid', [
                '<ul><li>Bots that trap customers with no way to reach a person.</li><li>Broadcasting to contacts who never opted in.</li><li>Long, robotic replies. One clear answer and one next step works best.</li><li>Setting it up once and never reading the conversations again.</li></ul>']),
        ],
        faqs=[
            ('Is WhatsApp automation legal in India?', ['Yes, when you use WhatsApp\'s official tools and follow its policies, including customer opt-in for business-started messages.']),
            ('Do I need the WhatsApp API to automate?', ['Not always. The free WhatsApp Business app covers greetings, away messages and quick replies. Flows, multiple agents and CRM connections need the WhatsApp Business Platform.']),
            ('Can automation hand a chat to a person?', ['Yes. A good setup passes complex or high-value conversations to your team and notifies the right person immediately.']),
        ],
        service='/ai-automation', need='automation'),
    dict(
        slug='instagram-dm-automation',
        tag='AI Automation',
        title='Instagram DM Automation: What Is Allowed and How to Set It Up',
        h1='Instagram DM automation',
        desc='Instagram DM automation explained: what Meta allows, comment-to-DM triggers, the 24-hour reply window, best uses for Indian brands and how to set it up safely.',
        read='6 min read',
        answer='Instagram DM automation sends instant, pre-written or AI-assisted replies to messages and comments on a professional Instagram account. It is allowed when it runs through Meta\'s official messaging tools or an approved partner, replies to people who contacted you first, and follows Meta\'s messaging window and policies.',
        sections=[
            ('What Instagram DM automation does', [
                'Most brands get the same questions in DMs and comments: price, size, availability, location, how to order. Automation answers those instantly, sends links people ask for, and collects details such as name, phone number or requirement, so your team picks up warm leads instead of starting from zero.']),
            ('What Meta allows', [
                '<ul><li>You need a professional Instagram account (business or creator) and an official integration, either Meta\'s own tools or an approved messaging partner.</li><li>Automated messages are replies to people who messaged you or commented first. Cold, unsolicited DMs are not allowed.</li><li>You can reply within 24 hours of a person\'s last message. Meta provides a limited extension for replies written by a human agent.</li><li>Follow Meta\'s community and messaging policies: no spam, no misleading content, and an easy way to reach a person.</li></ul>']),
            ('Comment-to-DM: the growth trigger', [
                'A popular pattern is the keyword trigger: a reel says "comment GUIDE and we will send it", and every comment with that word gets the link by DM. It boosts engagement on the post, gives people what they asked for instantly, and starts a conversation you can follow up on.']),
            ('Best uses for Indian brands', [
                '<ul><li><strong>Restaurants and cafés:</strong> menu, timings, offers and table booking links.</li><li><strong>Salons and clinics:</strong> service prices, slots and booking.</li><li><strong>D2C brands:</strong> product links, sizes, delivery questions and order status.</li><li><strong>Coaches and creators:</strong> lead magnets, course links and collab enquiries routed to the right inbox.</li></ul>']),
            ('How to set it up', [
                '<ol><li>Switch to a professional account and connect it to an approved automation tool.</li><li>List your top questions and write short, friendly replies in your brand voice.</li><li>Add keyword triggers for campaigns and reels.</li><li>Capture details only when they help, and send leads to a CRM or sheet.</li><li>Add a clear "talk to a person" option, then review conversations every month.</li></ol>']),
        ],
        faqs=[
            ('Will Instagram ban my account for using DM automation?', ['Not when you use official tools, reply only to people who contacted you, and stay within Meta\'s policies. Unofficial bots that mass-message strangers are what get accounts restricted.']),
            ('Can automation reply to comments too?', ['Yes. Keyword triggers can reply to a comment publicly and send the details by DM.']),
            ('Does it work for small accounts?', ['Yes. Small accounts often benefit most, because every enquiry matters and the owner cannot watch DMs all day.']),
        ],
        service='/ai-automation', need='automation'),
    dict(
        slug='ai-marketing-for-small-business-india',
        tag='AI Marketing',
        title='AI Marketing for Small Businesses in India: Where to Start',
        h1='AI marketing for small businesses in India',
        desc='A practical starting point for AI marketing in India: what AI does well, where people still matter, a 30-day plan and the mistakes to avoid.',
        read='8 min read',
        answer='AI marketing uses artificial intelligence for the parts of marketing that reward speed and data: researching trends and competitors, drafting posts and scripts, creating design and copy variations, answering messages and summarising results. Small businesses get the most from it when a person still sets the strategy, keeps the brand voice and approves what goes out.',
        sections=[
            ('What AI does well', [
                '<ul><li><strong>Research:</strong> spotting trends, competitor angles and the questions your customers ask.</li><li><strong>First drafts:</strong> captions, hooks, scripts, emails and ad copy in minutes.</li><li><strong>Variations:</strong> several versions of a headline or creative to test.</li><li><strong>Replies:</strong> instant answers to common DMs and WhatsApp questions.</li><li><strong>Reporting:</strong> turning numbers from several platforms into a plain summary.</li></ul>']),
            ('Where people still matter', [
                'AI does not know your customers, your margins or your reputation. Strategy, taste, local context, honesty in claims and the final check stay with people. The winning setup is AI for speed and people for judgement, so content is fast and still sounds like you.']),
            ('A 30-day starter plan', [
                '<ol><li><strong>Week 1, foundations:</strong> fix your Instagram bio, Google Business Profile and website basics. Write down your three main customer types and their top questions.</li><li><strong>Week 2, content system:</strong> use AI to draft a month of post ideas from those questions, then pick the best and make them in your brand style.</li><li><strong>Week 3, automation:</strong> set up instant replies for your most common DM and WhatsApp questions, with a handover to a person.</li><li><strong>Week 4, measure:</strong> track enquiries, bookings or sales from each channel, and keep what works.</li></ol>']),
            ('Tools to know', [
                'Assistants such as ChatGPT and Gemini for research and drafts, design tools such as Canva for quick creatives, Meta Business Suite for scheduling and inbox, and WhatsApp Business for customer chats. The tools matter less than the system: a clear plan, a consistent voice and a weekly review.']),
            ('Mistakes to avoid', [
                '<ul><li>Posting raw AI output that sounds generic or gets facts wrong.</li><li>Chasing every new tool instead of improving one channel at a time.</li><li>Measuring likes instead of enquiries and sales.</li><li>Making claims you cannot back up.</li></ul>']),
            ('When to get help', [
                'If you are spending more time making content than running the business, or leads go unanswered, a done-for-you partner pays for itself. An AI-driven growth company like Nxtlvl Social runs the system for you on a monthly subscription, with people reviewing every result.']),
        ],
        faqs=[
            ('Is AI marketing expensive for a small business?', ['It does not have to be. Many AI tools have free or low-cost plans, and the biggest saving is time. A done-for-you subscription costs less than hiring a full team.']),
            ('Will AI content hurt my brand?', ['Only if it is posted without review. Use AI for drafts and research, and let a person edit for accuracy and voice.']),
            ('What should I automate first?', ['Replies to your most common customer questions on WhatsApp and Instagram. It saves time immediately and stops leads slipping away.']),
        ],
        service='/ai-marketing', need='marketing'),
]
