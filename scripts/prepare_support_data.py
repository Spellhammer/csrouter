"""Materialize the curated synthetic Pie Calendar support seed (no API calls)."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTENTS = []


def add(label, title, source_ids, answer, train, calibration, test, **metadata):
    INTENTS.append(dict(label=label, title=title, source_ids=source_ids, answer=answer,
                        train=train.split("|"), calibration=calibration.split("|"), test=test.split("|"), **metadata))


add("create_event", "Create an event", [4],
    "Edit the WordPress post or page you want to use as an event. Enable Show on Calendar, set its start date and time, and optionally set an end date or mark it all-day. In Gutenberg the controls are in the sidebar; in the Classic Editor they are below the content. Display your events on a page using the Pie Calendar block or [piecal].",
    "How do I create my first event?|How do I make a WordPress post an event?|Where is Show on Calendar?|How do I set an event start date?|How do I create an all-day event?|Can a page become a calendar event?|How do I add a single event to Pie Calendar?|Where are the event controls in Classic Editor?|What are the steps to set up an event?|How do I mark a post to appear on the calendar?|How do I enter the start and end of an event?|How do I get started making events?",
    "I have a normal WordPress post and want to turn it into an event.|Where should I enter the date for my new event?|Can I schedule an all day gathering on my calendar?",
    "What do I switch on so this page is an event?|I'm new to Pie Calendar. How do I create an entry?|My workshop has no specific time; how do I add it?|I use the old WordPress editor; where do I enter event dates?")

add("display_calendar", "Display a calendar on a page", [5, 4],
    "Insert [piecal] on the page where you want the calendar to appear. If you use the WordPress Block Editor, you can insert the Pie Calendar block instead. Posts and pages must be configured as events with dates to appear in the calendar.",
    "What shortcode displays the calendar?|How do I put the calendar on my website?|What is the basic Pie Calendar shortcode?|How do I embed the event calendar in a page?|Where do I put [piecal]?|How do I display all my events in a calendar?|How do I add the calendar to my homepage?|What shortcode should I paste into WordPress?|Can I display a calendar without writing PHP?|How do I show my calendar on a landing page?|How do I insert the calendar in page content?|How do I publish the calendar view?",
    "Which shortcode do I need to show the calendar itself?|I created events; how do I display their calendar on a page?|Can I add the event calendar to my home page content?",
    "I need the embed shortcode for the whole calendar.|What do I paste into a page to display my events?|How can visitors see my event calendar on the site?|Is [piecal] the shortcode for showing the calendar?")

add("calendar_views", "Choose a calendar view", [5],
    "Set the view attribute on [piecal], for example [piecal view=\"listMonth\"] for a monthly list or [piecal view=\"timeGridWeek\"] for a weekly time grid. Documented choices include dayGridMonth, listMonth, timeGridWeek, listWeek, dayGridWeek, and listDay. The calendar block also exposes view controls.",
    "How do I change the default calendar view?|How do I show a weekly time grid?|How do I get a monthly list of events?|Which calendar views are available?|How do I use the view shortcode option?|Can I display a daily event list?|How do I change month view to week view?|How do I set timeGridWeek as default?|How do I use listWeek?|How do I use dayGridMonth?|How do I show a weekly grid of days?|How do I make listMonth the initial view?",
    "Can the calendar start in a weekly agenda view?|I want a list instead of the month grid.|What values does the view attribute accept?",
    "How can I show one day's event list?|Where do I select timeGridWeek?|I prefer a month-long agenda to boxes; what setting changes that?|Can the default display be listWeek?")

add("upcoming_events", "Show several months of upcoming events", [5],
    "Use [piecal view=\"listUpcoming\" duration=\"12\"] to show the next 12 months. The duration attribute supports up to 24 months and applies to listUpcoming and listMonthWithFeaturedImage. For the featured-image list, use [piecal view=\"listMonthWithFeaturedImage\" duration=\"6\"]; that view requires Pro. These controls are also available in the block.",
    "How do I show upcoming events for six months?|How do I list a whole year of future events?|What does the duration attribute do?|How do I use listUpcoming?|Can I display the next twelve months of events?|How do I show future events across several months?|How do I make a list of upcoming events with images?|What is the maximum duration in months?|Can I use duration in the month grid?|How do I show six months with featured images?|How do I use listMonthWithFeaturedImage?|How do I display sparse events over a year?",
    "We only have a few events annually; can the list span twelve months?|Which views support duration?|Can I list the next two years?",
    "I need an agenda covering the next half year.|Can the upcoming list stretch across 24 months?|How do I make future listings show thumbnails for six months?|Is listMonthWithFeaturedImage a Pro feature?")

add("calendar_locale", "Change calendar language", [5, 40],
    "The calendar normally uses your WordPress site's locale. To set a different calendar language, use the locale attribute, for example [piecal locale=\"es\"] for Spanish. For plugin interface strings, the internationalization guide describes translating with a plugin such as Loco Translate; check translated results on the front end.",
    "How do I change the calendar to Spanish?|How do I set the calendar language?|What is the locale shortcode parameter?|Can the calendar display French?|How do I translate calendar labels?|Does the calendar use the WordPress locale?|How do I override the site's calendar language?|How do I use locale es?|How do I translate plugin strings with Loco Translate?|How do I localize Pie Calendar?|Can I have a calendar in a different language?|Where do I set a language code?",
    "Can I force Spanish even though WordPress is English?|How do I translate the calendar's interface labels?|Which parameter sets the locale?",
    "I want French calendar labels on my English site.|Can I use Loco Translate with this plugin?|How can I override the inherited WordPress language?|What does locale=es change?")

add("calendar_theme", "Set dark or adaptive calendar theme", [5],
    "Use [piecal theme=\"dark\"] to force dark mode, or [piecal theme=\"adaptive\"] to follow the visitor's operating-system color-scheme preference. Test adaptive mode with your WordPress theme: if the site theme does not adapt too, calendar text can become difficult to read.",
    "How do I enable dark mode?|Can the calendar follow system dark mode?|What does theme adaptive mean?|How do I force the calendar dark?|How do I set the theme shortcode parameter?|Does Pie Calendar have a dark theme?|Why should I test adaptive theme colors?|How do I use theme dark?|How do I match the visitor's color scheme?|How do I switch calendar appearance to dark?|Can dark mode change automatically?|Will adaptive mode follow my operating system?",
    "Can the calendar switch between light and dark automatically?|I want dark mode on all the time.|How do I follow prefers-color-scheme?",
    "What shortcode forces a dark calendar?|Can visitors' OS appearance determine the calendar theme?|Does adaptive appearance also change my WordPress theme?|How do I configure the calendar's dark color scheme?")

add("wrap_titles", "Wrap long event titles", [5],
    "Add wraptitles to your shortcode, for example [piecal wraptitles=\"true\"]. Long event names will wrap within their calendar cells instead of being cut off by the cell boundaries.",
    "How do I wrap long event titles?|My event names are cut off in calendar cells.|How do I enable wraptitles?|Can long titles span multiple lines?|How do I stop calendar titles being truncated?|How do I show the full event name?|How do I wrap event text in the month grid?|What does wraptitles true do?|How do I make lengthy event names visible?|How do I prevent title clipping?|Can event names wrap rather than truncate?|How do I set title wrapping in the shortcode?",
    "Some calendar event names are too long for the boxes.|Is there a shortcode setting to wrap titles?|I want multi-line names in event cells.",
    "The end of each long event name disappears; can it wrap?|How do I turn on wraptitles=true?|Can the month cells display names on several lines?|What's the option that prevents clipped event titles?")

add("mobile_widget", "Use mobile or sidebar widget mode", [5],
    "Use [piecal widget=\"true\"] to keep widget mode on, or [piecal widget=\"responsive\"] to enable it at screen widths of 768px or less. Widget mode works only with the default Month - Classic / dayGridMonth view.",
    "How do I make the calendar work as a sidebar widget?|What does widget responsive do?|How do I enable mobile widget mode?|Can I force widget mode all the time?|How do I use widget true?|At what width does responsive widget mode activate?|Does widget mode support week views?|Can I make the calendar compact on phones?|How do I place a widget-style calendar in the sidebar?|Which view supports widget mode?|How do I change to widget mode only on small screens?|What is the responsive calendar widget setting?",
    "Can the calendar use its compact layout only on mobile?|I need widget mode permanently enabled.|What is the responsive widget breakpoint?",
    "Does widget=responsive work with timeGridWeek?|I want a compact month calendar for my narrow sidebar.|How do I enable the mobile layout below 768 pixels?|Which shortcode setting makes the calendar behave as a widget?")

add("automatic_end_dates", "Disable automatic one-hour end dates", [5],
    "For events without an explicit end date, Pie Calendar supplies an end date one hour after the start by default. Disable that behavior with [piecal automaticEndDates=false].",
    "Why does an event with no end date last an hour?|How do I disable automatic end dates?|What does automaticEndDates false do?|How do I stop the one hour default duration?|Do events get an end time automatically?|Why is an end time added when I leave it blank?|How do I turn off inferred end dates?|Can I leave an event end date unset?|How do I prevent automatic event endings?|Where do I disable automaticEndDates?|Why does my event have a default end time?|Is one hour the default duration without an end?",
    "I leave the end blank but the calendar adds an hour.|Which attribute stops an automatic end date?|How do I disable the default one-hour ending?",
    "Why is my no-end event shown as sixty minutes?|Can Pie Calendar stop inventing an end time?|How do I set automaticEndDates to false?|What happens if no end date is provided?")

add("recurring_events", "Configure recurring events and blackouts", [17],
    "Recurring events require Pie Calendar Pro. Edit the event, open Event Recurrence, and choose + Add Rule. A Recurrence Rule sets interval, frequency, weekdays, start, and stop dates; Single Recurrence adds one extra occurrence. Use Blackout Rule or Blackout Date/Range to exclude occurrences. Weekly rules support multiple weekdays. Monthly rules can use REPEAT ON or Same Weekday & Position; avoid combining those two monthly options.",
    "How do I create recurring events?|Can an event repeat every week?|How do I exclude holidays from recurrence?|What is a blackout rule?|How do I add a single extra recurrence?|How do I stop a recurring event on a date?|Can events repeat on Monday and Wednesday?|How do I repeat on the first Monday monthly?|Where is the Event Recurrence box?|Do recurring events require Pro?|How do I set a weekly recurrence interval?|How do I use Same Weekday and Position?",
    "Can one class repeat on Tuesdays and Thursdays?|I need to remove a holiday from a repeating series.|How do I make the event recur every three months?",
    "Where do I add a rule that repeats my event?|Can I schedule the last Friday of every month?|How do I set a final date for the repeating schedule?|What's the difference between a recurrence rule and a blackout rule?")

add("post_type_filter", "Filter the calendar by post type", [5, 22],
    "Use the type attribute with the actual WordPress post-type slug, for example [piecal type=\"event\"]. The calendar otherwise includes posts designated as events. Pro supports a comma-separated list of post types, for example [piecal type=\"events, post\"].",
    "How do I show only one post type?|How do I filter the calendar to an events CPT?|What does the type shortcode parameter do?|Can I display only products on this calendar?|How do I show events and posts together?|Can type accept multiple post types?|How do I set type event?|What slug goes in the type attribute?|How do I exclude other post types from a calendar instance?|Can I create a calendar for one CPT?|How do I limit the calendar to my event post type?|Does multiple post type filtering require Pro?",
    "I want this calendar to contain only my courses post type.|Can I pass events and post together in type?|Which attribute filters by WordPress post type?",
    "How do I restrict one calendar to products?|Does type=event mean the CPT slug?|I need a calendar showing two different post types.|Can each calendar instance select its own post type?")

add("custom_post_type_setup", "Enable calendar controls on a custom post type", [14],
    "For your custom post type, enable Editor and Custom Fields in its Supports settings. When editing with Gutenberg, also enable Show in REST API. This applies to post types registered through tools such as CPTUI, ACF, and Meta Box. In ACF Pro, enable Advanced Configuration to access the Supports settings.",
    "Why are Pie Calendar controls missing from my custom post type?|How do I enable event fields on an ACF CPT?|Which CPT Supports settings are required?|Does my post type need Show in REST API?|How do I configure CPTUI for Pie Calendar?|Where are calendar meta boxes on a custom post type?|How do I enable Custom Fields support?|Does the CPT need Editor support?|How do I use an ACF Pro post type with Pie Calendar?|How do I set up Meta Box custom post types?|How do I make event controls appear in Gutenberg for my CPT?|Where is ACF Advanced Configuration?",
    "The event sidebar is absent when editing my custom courses post type.|Which Supports options should I enable in CPTUI?|How do I get Pie Calendar fields on an ACF-created post type?",
    "My CPT editor has no calendar options; what registration settings matter?|Do I need REST API support for Gutenberg event controls?|Where does ACF hide the Supports configuration?|Can a Meta Box custom post type expose Pie Calendar's event fields?")

add("taxonomy_filter", "Filter events by categories or taxonomy terms", [22],
    "In Pro, use taxonomy and terms to filter the event query, for example [piecal taxonomy=\"category\" terms=\"Concerts\"]. Multiple terms can be comma-separated. The operator defaults to IN; documented alternatives include NOT IN, AND, EXISTS, and NOT EXISTS. Use the taxonomy and term values appropriate to your site.",
    "How do I filter events by category?|How do I show only one taxonomy term?|What does the taxonomy shortcode option do?|How do I use terms with a category?|Can I exclude a category from the calendar?|How do I use operator NOT IN?|Can the calendar filter by several taxonomy terms?|How do I show all posts that have a category?|Do category filters require Pro?|How do I use the terms attribute?|Can I filter events using a custom taxonomy?|Which taxonomy operators are available?",
    "Can I make a calendar just for Concerts category events?|I want to exclude the Outdoors taxonomy term.|How do I set multiple terms for a taxonomy filter?",
    "What attributes limit events to a specific category?|Can operator=NOT IN hide certain event categories?|I need to filter a calendar by my custom event taxonomy.|Is taxonomy filtering available in the free plugin?")

add("builder_compatibility", "Page-builder and theme compatibility", [34],
    "The compatibility guide lists Gutenberg, Classic Editor, Beaver Builder, Elementor, GeneratePress, and Divi as fully compatible. In Oxygen and Bricks, the [piecal] shortcode may not fully render inside the builder, but should render on the front end. Check the live page when the builder preview is incomplete; unresolved issues should go to support.",
    "Does Pie Calendar work with Elementor?|Does it support Divi?|Why is the shortcode preview missing in Bricks?|Can I use Pie Calendar with Oxygen Builder?|Which page builders are compatible?|Will Pie Calendar work with GeneratePress?|Is Beaver Builder supported?|Why does the calendar render on the front end but not in Oxygen?|Does Classic Editor work with Pie Calendar?|Can I use the calendar in Bricks Builder?|How do I check builder compatibility?|Is the incomplete Bricks preview a known issue?",
    "The Oxygen canvas doesn't show the calendar but the live page does.|Is Elementor on your compatibility list?|Can I use this plugin with Beaver Builder?",
    "Should I expect the shortcode to render completely in Bricks' editor?|Is GeneratePress compatible with Pie Calendar?|Does your calendar integrate with Divi pages?|Which of Oxygen or Gutenberg has a preview limitation?")

add("block_editor", "Add the calendar or event-info block", [71],
    "In the WordPress Block Editor, open the page or post, click Add Block (+), search for Pie Calendar, and select the calendar block. Configure its options in the editor. Use Pie Calendar Event Info for individual event details. To migrate an existing calendar shortcode, add the block, select equivalent settings, and remove that shortcode. Shortcodes remain supported.",
    "How do I add the Pie Calendar block?|Can I use Gutenberg without shortcodes?|How do I migrate a shortcode to a calendar block?|Where are the block settings?|How do I insert the Event Info block?|Which Pie Calendar blocks exist?|How do I find Pie Calendar in Add Block?|Can I still use shortcodes after adding blocks?|How do I configure the calendar visually in Gutenberg?|Does the plugin support the WordPress Block Editor?|Can I mix blocks and shortcodes?|How do I add a calendar using the plus button?",
    "I prefer Gutenberg controls rather than shortcode attributes.|How do I replace my old shortcode with the block?|Where do I find the calendar block in WordPress?",
    "Can I configure Pie Calendar directly in the block sidebar?|Which block displays single-event information?|I want to insert the calendar through Add Block.|Will existing shortcodes keep working on a block-editor site?")

add("add_to_calendar", "Enable visitor Add to Calendar links", [30],
    "Add to Calendar links require Pro and are off until enabled. In WordPress go to Settings > Pie Calendar and choose the calendars to show in the event popover. Supported destinations include Google Calendar, Office365, and ICS files for calendars such as Apple and Outlook. On a single-event page, use [piecal-info fragments=\"atc\"] to display only those links.",
    "How do I enable Add to Calendar links?|Can visitors save an event to Google Calendar?|How do I show Apple Calendar links?|Where are the Add to Calendar settings?|Why are Add to Calendar links not visible by default?|How do I put calendar export links on a single event?|What does fragments atc do?|Does Add to Calendar require Pro?|Can visitors download an ICS file for an event?|How do I enable Office365 calendar links?|How do I show Outlook add-to-calendar links?|How do I choose calendars in the event popover?",
    "Can visitors add my event to their personal calendar?|I need just the Add to Calendar buttons on an event page.|Where do I turn on the Google Calendar export link?",
    "How do I let someone save one event into Apple Calendar?|What setting enables ATC links in the popover?|Can I display only fragments=atc on a post?|Are the visitor calendar links a Pro-only feature?")

add("adaptive_timezone", "Understand or disable adaptive time zones", [31],
    "The Pro adaptive-time-zone guide explains that event times are converted from the WordPress time zone (Settings > General) to each visitor's detected local time zone, including daylight saving time. To keep the calendar from adapting, use [piecal adaptiveTimeZone=false], or disable the corresponding block control. The visitor's detected zone is displayed below the front-end calendar.",
    "Why do visitors see different event times?|How do I disable adaptive time zones?|Where does the calendar get its time zone?|How do I make everyone see the site time?|Does the calendar adjust for daylight saving?|What does adaptiveTimeZone false do?|How do I stop timezone conversion?|Where do I set the WordPress time zone?|Why does an event time change for another country?|How do I see the detected visitor timezone?|Can I turn off timezone adaptation in the block?|How does Pie Calendar handle local time zones?",
    "My visitor sees 8:30 but I entered 9:30 in New York.|Can all users see the original site timezone?|Does adaptive timezone account for daylight savings?",
    "How do I prevent times from changing for overseas visitors?|What setting controls the calendar's base timezone?|Why is a detected timezone displayed below the calendar?|Can I set adaptiveTimeZone=false in my shortcode?")

add("event_info", "Show dates and times on individual event pages", [85],
    "Use [piecal-info] or the Pie Calendar Event Info block on a single-event post or template. Select fragments such as start, end, timezone, allday, or all; for example [piecal-info fragments=\"start, timezone\"]. Pro also supports atc for Add to Calendar links. Date/time formatting defaults to WordPress settings and can be overridden using the format attribute with PHP date-format characters.",
    "How do I show event dates on a single post?|What is the piecal-info shortcode?|How do I display just the start time?|Can I show the event timezone on its page?|How do I use fragments start and end?|How do I format the event info date?|Which fragments does piecal-info support?|How do I add event details to a single event template?|Can the Event Info block show dates?|How do I show all day status on a post?|How do I change piecal-info format?|Can I use multiple event info shortcodes?",
    "My single-event page needs a start date and timezone.|Which shortcode prints the event's dates rather than a calendar?|Can I format dates in the event info output?",
    "How do I display the start and finish on each event page?|What does fragments=all output?|Can I add an Event Info block to my single post template?|How do I control the format parameter in piecal-info?")

add("custom_date_fields", "Use existing custom fields for event dates", [23],
    "The developer guide supports existing date/time meta fields through piecal_event_query_args, piecal_start_date_meta_key, and piecal_end_date_meta_key. Its ACF example assumes Date Time Picker fields with the default return format. This changes the event query: only posts with the designated custom start field appear, and the native start/end controls and Show on Calendar toggle are ignored. Follow the linked example with your field names; site-specific code changes need developer review.",
    "Can Pie Calendar use my ACF date fields?|How do I use custom fields as event dates?|Can existing custom start times drive the calendar?|Which filters change the date meta keys?|What ACF date field return format works?|Why are native date fields ignored with custom date integration?|Can I use Meta Box event dates?|How do I set piecal_start_date_meta_key?|How do I set piecal_end_date_meta_key?|Does custom start field integration change Show on Calendar?|Can I reuse a pre-existing events CPT's dates?|How do I map ACF start and end date fields?",
    "I already store event dates in ACF Date Time Picker fields.|Can the calendar read custom_event_start instead of its own start field?|Will native event toggles still apply after replacing the date query?",
    "How do I connect existing custom start and finish meta keys?|Which hooks tell Pie Calendar where my dates are stored?|Why do only events with my custom start field appear now?|Does the ACF custom-date integration use the default return format?")

add("event_colors", "Set event colors by event or taxonomy", [37],
    "Pro provides per-event color and text-color options. For automatic colors based on category, taxonomy term, or custom post type, the developer guide uses piecal_event_array_filter to change color and textColor on each event. Use the linked examples as a starting point and adapt the taxonomy, term slugs, post-type slug, and colors to your site.",
    "How do I set event colors by category?|Can each event have a different color?|How do I color events by post type?|Which hook changes event color?|How do I set the text color on events?|Can taxonomy terms determine event colors?|Does per-event color require Pro?|How do I change color and textColor?|How do I make all Green Events green?|Can I color-code custom post types?|How do I automatically assign colors by taxonomy?|Where is the category color code example?",
    "I want concerts and workshops to have different colors.|Can the event array filter set textColor?|How do I apply one color to all events of a CPT?",
    "Can a taxonomy term choose my event dot color?|Which Pro options change an event's foreground color?|Where can I find the code for coloring events by category?|How do I color-code event types automatically?")

add("popover_image", "Show featured images in event popovers", [51],
    "In Pie Calendar Pro 1.3.2 or later, add featuredimage=true to your calendar shortcode, for example [piecal featuredimage=true]. The event uses the post's featured image in its popover. The linked guide also points to the developer approach for adding custom fields to popover content.",
    "How do I show a featured image in the popover?|What does featuredimage true do?|Can the event popup show a thumbnail?|How do I enable post images in event details?|Does the popover image require Pro?|Which version adds featured images in popovers?|How do I put the post featured image in the calendar popup?|Can I add images to event popovers?|How do I use the featuredimage shortcode attribute?|How do I show an image when clicking an event?|Can popover details include the featured picture?|How do I enable event popup images?",
    "I want a photo inside the event popover when clicked.|Is featuredimage=true available in Pro?|How do I display the post thumbnail in the popup?",
    "What attribute adds the featured picture to the event popover?|Does Pro 1.3.2 support popover photos?|Can I show an event's WordPress featured image in its details popup?|How do I activate thumbnails after clicking a calendar entry?")

add("skip_popover", "Open the event page or a custom URL directly", [29, 48],
    "The documentation provides a developer snippet using piecal_additional_event_click_js to skip the popover and open the event page. For a custom URL field, the separate guide uses piecal_event_array_filter and click JavaScript; its sample assumes ACF. Follow the linked snippet appropriate to the desired destination. Adapting custom PHP/JavaScript to your site should be reviewed by a developer.",
    "How do I skip the event popover?|Can clicking an event go straight to its post?|How do I send event clicks to a custom URL?|Can I bypass the event popup?|How do I link events to an external ticket page?|How do I use an ACF URL for event clicks?|Which hook changes event click behavior?|How do I open the permalink immediately?|Can event clicks redirect without showing details?|How do I use customLink in an event?|How do I disable the popover on click?|Can I use a custom URL as the popover link?",
    "I want the click to open the event page without a popup.|Can an ACF link field send people straight to another URL?|Which guide covers skipping the popover?",
    "How do I bypass the details panel and redirect visitors?|Can a calendar entry point directly to an external registration page?|Is there a snippet that opens the post permalink on click?|How do I change the event link to my custom URL field?")

add("frontend_submissions", "Accept event submissions from site visitors", [7, 8],
    "Use a capable front-end form plugin that can create WordPress posts and map submitted values to Pie Calendar's event meta fields. The tutorial demonstrates Gravity Forms with its Advanced Post Creation add-on; it also mentions Fluent Forms and WS Forms as alternatives. Map the event flag and correctly formatted date/time fields using the meta-field reference. This is a form-plugin integration, not a built-in submission form.",
    "Can visitors submit calendar events?|How do I make a front end event submission form?|Does Pie Calendar have a built-in submission form?|Can Gravity Forms create calendar events?|How do I map form fields to event meta?|Can Fluent Forms submit events?|Can WS Forms create event posts?|What is the front end submission tutorial?|Which Gravity Forms add-on creates event posts?|Can a community website accept event listings?|How do users add events without wp-admin?|How do I connect a form to calendar events?",
    "I'd like community members to submit listings from the website.|Can a form create posts that appear on the calendar?|Which form plugin does your submission tutorial demonstrate?",
    "Can I collect event dates using Gravity Forms Advanced Post Creation?|Do visitors need wp-admin to submit an event?|How do I connect a front-end form to the event fields?|Does Pie Calendar itself provide the submission form?")

add("csv_import", "Import events from a spreadsheet or CSV", [49, 8],
    "Export your spreadsheet as CSV and use an import tool that maps columns to WordPress posts and custom fields; WP All Import Pro is one documented example, not a requirement. Map the post title and Pie Calendar meta fields, including _piecal_is_event with value 1 and the date fields. Follow the meta-field reference for exact formats. Pie Calendar support does not cover third-party import plugins.",
    "How do I import events from CSV?|Can I import an Excel event spreadsheet?|Does WP All Import work with Pie Calendar?|How do I map CSV columns to event meta?|Can I import Google Sheets events?|Is WP All Import Pro required?|Which fields does an event CSV need?|What value goes in _piecal_is_event?|How do I bulk import event posts?|Can I upload a spreadsheet of dates?|How do I import a list of calendar events?|Where is the CSV import guide?",
    "I have hundreds of events in a spreadsheet to bring into WordPress.|Can an importer map columns into Pie Calendar fields?|Must I use WP All Import Pro for event CSVs?",
    "How do I migrate Excel rows into event posts?|Does the CSV event flag need the value 1?|Can I use another CSV tool with custom-field mapping?|Where do I find the meta formats for bulk event importing?")

add("license_upgrade", "Upgrade to an unlimited-site license", [20],
    "Sign in at https://piecalendar.com/my-account/, choose View Licenses, then View Upgrades beside your license. Select Upgrade License and complete checkout. The guide describes paying the difference to the unlimited-site license and continuing to use the existing license key. For questions about your specific purchase, eligibility, or a failed checkout, contact a human representative.",
    "How do I upgrade to unlimited sites?|Can I upgrade my five-site license?|Where is View Upgrades in my account?|How do I change my Pie Calendar license tier?|Do I keep my key after upgrading?|How do I buy the unlimited license upgrade?|What are the steps to upgrade a license?|Where do I find Upgrade License?|Can I expand the number of licensed sites?|How do I upgrade an existing Pro license?|Do license upgrades use the existing key?|How do I move from limited sites to unlimited?",
    "I own a smaller license and want unlimited sites.|Where in my account can I upgrade my site allowance?|Does upgrading require a new license key?",
    "How do I increase my existing license to unlimited installations?|What button in View Licenses starts the upgrade?|Will my current key work after the unlimited upgrade?|What is the documented process for moving to the unlimited tier?")

add("invoice_update", "Download or update an invoice", [45],
    "After purchasing Pro, sign in at https://piecalendar.com/my-account/ and select View Invoice. To edit the billing details or add VAT information, choose Update at the upper right, enter the details, then select Save Billing Details & Generate Invoice. You can then download the updated PDF invoice. A dispute, tax advice, or a problem with a specific charge requires human assistance.",
    "How do I download my invoice?|How do I add VAT information to an invoice?|Where do I edit invoice billing details?|Can I get a PDF invoice?|How do I change the company name on my invoice?|Where is View Invoice?|How do I regenerate an invoice with new details?|How do I add my VAT number?|Where is Save Billing Details and Generate Invoice?|Can I update my billing address on the invoice?|How do I download a receipt from my account?|What is the invoice Update button for?",
    "I need my business address printed on a PDF invoice.|Can I add a VAT ID after purchasing?|Where do I generate the revised invoice?",
    "How can I download a purchase invoice as PDF?|My accountant needs our VAT details on the invoice.|Where do I update the company billing information?|Which account page control regenerates an invoice?")

add("connector_ics", "Display external ICS feeds", [83, 91],
    "Install and configure the Pie Calendar Connector add-on to display external ICS feeds. It works with the free Pie Calendar plugin as well as Pro. In the calendar block, expand Event Sources, enable ICS, and paste the feed URL. With a shortcode, use sources=\"ics\" and supply the URL through icsurls; multiple feed URLs can be comma-separated. This imports feed events for display; it is distinct from visitors exporting a single event.",
    "How do I display a Google Calendar feed?|Can I import an ICS feed into Pie Calendar?|How do I configure icsurls?|Does ICS integration require the Connector?|Can I show multiple ICS feeds?|How do I enable ICS in Event Sources?|Can I display a Basecamp calendar feed?|What does sources ics mean?|Does Connector work with free Pie Calendar?|How do I paste a feed URL into the block?|Can I pull external calendar events into WordPress?|How do I add an iCalendar subscription feed?",
    "Can I pull my Google Calendar events into the website calendar?|Where do I enter an external ICS URL?|How do I combine two ICS feed URLs?",
    "What add-on reads an external iCalendar feed?|Can I display a Basecamp ICS source on my site?|How do sources=ics and icsurls work together?|Can I use the Connector ICS feature without Pie Calendar Pro?")

add("connector_eventbrite", "Connect and display Eventbrite events", [83, 90],
    "Use the Pie Calendar Connector add-on. Create an Eventbrite API key and copy its private token. In WordPress go to Settings > Pie Calendar Connector, save the token, select your Eventbrite Organization ID, save again, and choose Synchronize Eventbrite Events. Enable Eventbrite under the block's Event Sources, or use [piecal sources=\"eventbrite\"]. Use sources=\"native, eventbrite\" to include native events too. Enter tokens in your admin settings, not in support chat.",
    "How do I connect Eventbrite?|How do I show Eventbrite events in WordPress?|Which Eventbrite token does Connector need?|Where do I save the Eventbrite private token?|How do I choose my Eventbrite organization?|How do I synchronize existing Eventbrite events?|How do I enable the Eventbrite source?|Can I show native and Eventbrite events together?|Does Connector display Eventbrite events?|What is Synchronize Eventbrite Events?|How do I create an Eventbrite API key for Connector?|How do I use sources eventbrite?",
    "How do I pull my Eventbrite organization events into Pie Calendar?|Where does the Eventbrite private token go?|Can I mix Eventbrite events and WordPress events?",
    "What are the initial steps to connect my Eventbrite organization?|Which source checkbox displays synced Eventbrite events?|Do I use the public or private token in Connector settings?|How can I show Eventbrite alongside native entries?")

add("connector_webhooks", "Keep Eventbrite changes synchronized", [90],
    "In Eventbrite go to Account Settings > Developer Links > Webhooks and add a webhook with your site's URL followed by /wp-json/piecal-connector/v1/webhook/update. Enable event.created, event.published, event.unpublished, and event.updated. Save and test it; a successful test returns HTTP 200. Updates can take several minutes. For 400/403 responses, inspect the response body; persistent errors need human investigation.",
    "How do I set up Eventbrite webhooks?|Why aren't Eventbrite edits instantly synchronized?|What is the Connector webhook URL?|Which Eventbrite webhook actions are required?|How do I test an Eventbrite webhook?|What status code means webhook success?|Can I keep Eventbrite changes updated automatically?|Where do I configure webhooks in Eventbrite?|How long do Eventbrite webhook updates take?|How do I sync event.updated changes?|Where is the webhook Recent Requests log?|How do I avoid manually synchronizing Eventbrite?",
    "I need edits in Eventbrite to update my WordPress events automatically.|Which webhook endpoint should I configure?|Is a delay of several minutes normal for Eventbrite changes?",
    "What actions should my Eventbrite webhook subscribe to?|How do I check whether a webhook test succeeded?|Does Eventbrite send updates instantly?|Where do I see the response body of a failed webhook test?")

HUMAN_TRAIN = """I need a human support representative.|Please let me talk to a real person.|Can an agent help me directly?|I want a refund for my purchase.|I was charged twice for Pie Calendar.|My license activation fails on my site.|Can you look up my license key?|I lost access to my account email.|My renewal payment was declined.|Can you cancel my subscription for me?|I need to dispute a charge.|My account has been hacked.|The latest update crashed my site.|The calendar is completely broken and I need you to investigate.|I already tried the documentation and it still fails.|My events vanished and I need help recovering them.|Please log into my website to fix this.|Can you write a custom integration for my site?|I need a custom PHP fix for this stack trace.|My Eventbrite token is rejected even after following all setup steps.|The webhook returns 403 and nothing in the guide helps.|My imported CSV dates are corrupt; investigate my data.|I need legal advice about accessibility compliance.|Can you guarantee WCAG compliance for my entire site?|What is your refund policy?|What is the current price of Pro?|Are there any discount codes today?|Can you give me a custom quote?|Which subscription did I buy?|Please retrieve my invoice for order 12345.|Can you send my API token to me?|I need someone to debug a conflict with my custom theme.|Why is my checkout failing?|My license upgrade failed after I paid.|Tell me the weather tomorrow.|Write a recipe for apple pie.|Can you book a flight for me?|How do I fix my printer?|Who won yesterday's football match?|What is the meaning of life?|I need password reset help for my Pie Calendar account.|Can you change the email address on my account?|My calendar isn't working.|Help please.|It doesn't work.|The dates are wrong and I've checked the timezone already.|I'm reporting a reproducible plugin bug.|Give me a SQL command to delete all events.|Can you create a custom booking and ticketing system?|Why is my site so slow after enabling the plugin?|I need payment and refund assistance.|Reset my activation limit for me.|I already enabled the popover image setting but images are still missing.|The shortcode is correct but no calendar renders on the live site.|I followed the recurring rule guide but occurrences are still missing.|Can you restore my deleted Eventbrite entries without API access?|How do I reset passwords in WooCommerce?|How do I change my Google Calendar account password?|How do I configure a calendar on Shopify?|Can you show a custom solution using my private code?|What features will ship next month?|Does Pie Calendar handle event capacity and seat reservations?|I need help with a security vulnerability.|I want both a refund and help adding an event."""
HUMAN_CAL = """Please transfer me to your support team.|The site throws a fatal PHP error after the update.|Can you check the status of my particular payment?|What's the current renewal price?|My activation limit needs resetting.|I need custom code for a private client project.|Can you fix an invoice dispute for me?|Write a poem about a pie.|I have no idea what's wrong; it just fails.|I tried the ICS setup but the feed still cannot load.|Give me a refund and tell me how to show the calendar.|I need legal assurances that this site is accessible."""
HUMAN_TEST = """I want someone from support, not an automated answer.|Please refund order 7788.|My account says the key is invalid; investigate.|I can't log into the Pie Calendar purchase account.|The calendar still doesn't show anything after I followed every setup step.|My site gives a fatal error with your plugin.|Please fix my rejected Eventbrite credentials.|The images are blank even with featuredimage=true.|Can you review the PHP exception from my production server?|I want to know today's subscription price.|What discount is available this weekend?|When will you add a ticket reservation feature?|I need tax advice for my invoice.|Tell me how to bake a chocolate cake.|Explain how to cancel Netflix.|What is the forecast in London?|Can you look up invoice 555 for my order?|I need a person to reset my site activation count.|The feed has stopped working and the guide didn't resolve it.|Can you take payment from me in this chat?|My license upgrade charged me but didn't activate.|Does this plugin sell tickets with seat limits?|The calendar is broken; I can't describe it.|Can you reset my WordPress admin password?|Please erase all calendar data with SQL.|Help me with the WooCommerce checkout error.|My monthly repeats are missing despite the correct rules.|How do I both configure recurring events and upgrade my license?|How can I switch to dark mode and import my Eventbrite organization?|Can you show tomorrow's train timetable?"""


LICENSE_EXAMPLE = "I tried to delete the license on my site, save the settings, re-load the page, past the correct license in, and save the settings, then UPDATE PLUGIN... that still results in an unauthorized download. It simply won't authenticate."

add("license_activation", "License activation and unauthorized plugin downloads", [],
    "Please contact our team at support@piecalendar.com for help with licensing related issues.",
    "How do I activate my Pie Calendar Pro license?|My Pie Calendar plugin update returns an unauthorized download.|I entered my license but the plugin won't authenticate.|Where do I activate a saved license key?|How do I re-enter a license to authorize plugin updates?|I saved the correct license and the Pro update still fails to authenticate.|The update download says unauthorized after clearing and saving my license.|Does saving my license key activate it?|Replacing my license key still won't authorize the plugin download.|How can I check my license activation?|My license activation fails on my site.|My website cannot validate my Pro license for updates.|I removed the old license and pasted the new key but authentication fails.|The plugin says my license key is invalid when I try updating.|Who can help with a license authentication issue?|How do I resolve licensing-related problems with Pie Calendar?",
    "My license is saved but plugin updates report unauthorized.|The Pro license won't activate on this website.|Who should I contact about license authentication failures?|I cleared and re-entered the license but the updater still can't authenticate.|How do I get help with Pie Calendar licensing issues?",
    "The license settings save correctly but I can't authorize a plugin update.|I pasted my valid Pro key and the download is refused as unauthorized.|Where can I get support for license activation problems?|The website rejects my license when downloading the latest version.|I deleted the stored key and reloaded settings; it still won't authenticate.|Does your team handle problems activating a license key?|My licence key won't validate for Pie Calendar plugin updates.|" + LICENSE_EXAMPLE,
    review_status="approved_by_product_owner", response_type="support_referral",
    handoff={"method": "email", "email": "support@piecalendar.com", "url": "mailto:support@piecalendar.com"},
    sources=[{"type": "product_owner_instruction", "title": "Product-owner approved licensing support response", "provided_on": "2026-10-10"}])

# This troubleshooting question now has a specific licensing referral instead of the generic human response.
HUMAN_TRAIN = "|".join(q for q in HUMAN_TRAIN.split("|") if q != "My license activation fails on my site.")


def write_csv(path, rows):
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "label", "source_urls", "origin"])
        writer.writeheader()
        writer.writerows(rows)


def main():
    data = ROOT / "data/support"
    config_dir = ROOT / "config/support"
    data.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)
    source_index = json.loads((data / "sources.json").read_text())
    sources = {int(a["url"].split("/article/")[1].split("-")[0]): a for a in source_index["articles"]}
    config = {"schema_version": 1, "task_id": "csrouter", "product": "Pie Calendar",
              "model_pack": "models/jeffy", "review_status": "synthetic_draft_needs_human_review",
              "docs_fetched_at": source_index["fetched_at"], "default_threshold": 0.9,
              "minimum_margin": 0.15, "max_clarifications": 2,
              "fallback_label": "human_required",
              "fallback_answer": "I'm sorry, I'm not sure I can provide the assistance you're looking for. Let me send this conversation to a human representative and have them help you instead.",
              "handoff_url": "https://piecalendar.com/contact/", "routes": {}}
    splits = {name: [] for name in ("train", "calibration", "evaluation")}
    catalog = []
    for intent in INTENTS:
        refs = [sources[id] for id in intent["source_ids"]]
        route = {"title": intent["title"], "answer": intent["answer"], "enabled": True,
                 "threshold": 0.9, "review_status": intent.get("review_status", "needs_human_review"),
                 "sources": intent.get("sources", [{k: a[k] for k in ("url", "title", "last_updated", "sha256")} for a in refs])}
        for key in ("response_type", "handoff"):
            if key in intent:
                route[key] = intent[key]
        config["routes"][intent["label"]] = route
        catalog.append({k: intent[k] for k in ("label", "title", "source_ids", "train", "calibration", "test")})
        for name, questions in (("train", intent["train"]), ("calibration", intent["calibration"]), ("evaluation", intent["test"])):
            for q in questions:
                # Context augmentation belongs only to training; held-out questions are authored separately.
                variants = [q, "I'm using Pie Calendar on WordPress. " + q] if name == "train" else [q]
                for text in variants:
                    splits[name].append({"text": text, "label": intent["label"],
                                         "source_urls": " ".join(a["url"] for a in refs),
                                         "origin": "user_provided_regression" if text == LICENSE_EXAMPLE else
                                         "synthetic_product_owner_policy" if intent.get("sources") else "synthetic_documentation_based"})
    for name, questions in (("train", HUMAN_TRAIN), ("calibration", HUMAN_CAL), ("evaluation", HUMAN_TEST)):
        for text in questions.split("|"):
            splits[name].append({"text": text, "label": "human_required", "source_urls": "",
                                 "origin": "synthetic_escalation_policy"})
    for name, rows in splits.items():
        write_csv(data / f"{name}.csv", rows)
    (config_dir / "routes.json").write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n")
    (data / "intent_seeds.json").write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
    (data / "dataset.json").write_text(json.dumps({
        "task_id": "csrouter", "synthetic": True, "review_status": "needs_human_review",
        "labels": [i["label"] for i in INTENTS] + ["human_required"],
        "counts": {name: len(rows) for name, rows in splits.items()},
        "training_augmentation": "Answer routes use plain and product-context variants of unique question seeds: 12 seeds per original route and 16 for license_activation. These are not independent customer examples.",
        "split_policy": "Separate authored calibration and evaluation questions; no random split of augmented variants. Evaluation must not select thresholds.",
        "limitations": ["Synthetic questions do not establish real-customer accuracy.",
                         "English-only; unknown topics may receive high classifier confidence.",
                         "Answers require product-owner review before production use."]
    }, indent=2) + "\n")
    print(f"Prepared {len(INTENTS) + 1} labels: " + str({name: len(rows) for name, rows in splits.items()}))


if __name__ == "__main__":
    main()
