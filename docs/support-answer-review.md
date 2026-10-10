# Pie Calendar answer review

Documentation-based answers are drafts pending product-owner approval. The license_activation referral was approved directly by the product owner.

## Create an event

Label: `create_event` | automatic response: enabled | threshold: 0.85

Edit the WordPress post or page you want to use as an event. Enable Show on Calendar, set its start date and time, and optionally set an end date or mark it all-day. In Gutenberg the controls are in the sidebar; in the Classic Editor they are below the content. Display your events on a page using the Pie Calendar block or [piecal].

Sources:

- [4 Minute Quick Start Guide](https://docs.piecalendar.com/article/4-4-minute-quick-start-guide) (article updated 2025-11-07)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Display a calendar on a page

Label: `display_calendar` | automatic response: enabled | threshold: 0.85

Insert [piecal] on the page where you want the calendar to appear. If you use the WordPress Block Editor, you can insert the Pie Calendar block instead. Posts and pages must be configured as events with dates to appear in the calendar.

Sources:

- [Shortcode Options](https://docs.piecalendar.com/article/5-shortcode-options) (article updated 2026-01-28)
- [4 Minute Quick Start Guide](https://docs.piecalendar.com/article/4-4-minute-quick-start-guide) (article updated 2025-11-07)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Choose a calendar view

Label: `calendar_views` | automatic response: enabled | threshold: 0.85

Set the view attribute on [piecal], for example [piecal view="listMonth"] for a monthly list or [piecal view="timeGridWeek"] for a weekly time grid. Documented choices include dayGridMonth, listMonth, timeGridWeek, listWeek, dayGridWeek, and listDay. The calendar block also exposes view controls.

Sources:

- [Shortcode Options](https://docs.piecalendar.com/article/5-shortcode-options) (article updated 2026-01-28)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Show several months of upcoming events

Label: `upcoming_events` | automatic response: enabled | threshold: 0.85

Use [piecal view="listUpcoming" duration="12"] to show the next 12 months. The duration attribute supports up to 24 months and applies to listUpcoming and listMonthWithFeaturedImage. For the featured-image list, use [piecal view="listMonthWithFeaturedImage" duration="6"]; that view requires Pro. These controls are also available in the block.

Sources:

- [Shortcode Options](https://docs.piecalendar.com/article/5-shortcode-options) (article updated 2026-01-28)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Change calendar language

Label: `calendar_locale` | automatic response: enabled | threshold: 0.85

The calendar normally uses your WordPress site's locale. To set a different calendar language, use the locale attribute, for example [piecal locale="es"] for Spanish. For plugin interface strings, the internationalization guide describes translating with a plugin such as Loco Translate; check translated results on the front end.

Sources:

- [Shortcode Options](https://docs.piecalendar.com/article/5-shortcode-options) (article updated 2026-01-28)
- [Internationalization](https://docs.piecalendar.com/article/40-internationalization) (article updated 2024-04-25)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Set dark or adaptive calendar theme

Label: `calendar_theme` | automatic response: enabled | threshold: 0.85

Use [piecal theme="dark"] to force dark mode, or [piecal theme="adaptive"] to follow the visitor's operating-system color-scheme preference. Test adaptive mode with your WordPress theme: if the site theme does not adapt too, calendar text can become difficult to read.

Sources:

- [Shortcode Options](https://docs.piecalendar.com/article/5-shortcode-options) (article updated 2026-01-28)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Wrap long event titles

Label: `wrap_titles` | automatic response: enabled | threshold: 0.85

Add wraptitles to your shortcode, for example [piecal wraptitles="true"]. Long event names will wrap within their calendar cells instead of being cut off by the cell boundaries.

Sources:

- [Shortcode Options](https://docs.piecalendar.com/article/5-shortcode-options) (article updated 2026-01-28)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Use mobile or sidebar widget mode

Label: `mobile_widget` | automatic response: enabled | threshold: 0.85

Use [piecal widget="true"] to keep widget mode on, or [piecal widget="responsive"] to enable it at screen widths of 768px or less. Widget mode works only with the default Month - Classic / dayGridMonth view.

Sources:

- [Shortcode Options](https://docs.piecalendar.com/article/5-shortcode-options) (article updated 2026-01-28)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Disable automatic one-hour end dates

Label: `automatic_end_dates` | automatic response: enabled | threshold: 0.85

For events without an explicit end date, Pie Calendar supplies an end date one hour after the start by default. Disable that behavior with [piecal automaticEndDates=false].

Sources:

- [Shortcode Options](https://docs.piecalendar.com/article/5-shortcode-options) (article updated 2026-01-28)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Configure recurring events and blackouts

Label: `recurring_events` | automatic response: enabled | threshold: 0.85

Recurring events require Pie Calendar Pro. Edit the event, open Event Recurrence, and choose + Add Rule. A Recurrence Rule sets interval, frequency, weekdays, start, and stop dates; Single Recurrence adds one extra occurrence. Use Blackout Rule or Blackout Date/Range to exclude occurrences. Weekly rules support multiple weekdays. Monthly rules can use REPEAT ON or Same Weekday & Position; avoid combining those two monthly options.

Sources:

- [How to Configure Recurring Events](https://docs.piecalendar.com/article/17-how-to-configure-recurring-events) (article updated 2026-10-01)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Filter the calendar by post type

Label: `post_type_filter` | automatic response: enabled | threshold: 0.85

Use the type attribute with the actual WordPress post-type slug, for example [piecal type="event"]. The calendar otherwise includes posts designated as events. Pro supports a comma-separated list of post types, for example [piecal type="events, post"].

Sources:

- [Shortcode Options](https://docs.piecalendar.com/article/5-shortcode-options) (article updated 2026-01-28)
- [Shortcode Options [Pro Only]](https://docs.piecalendar.com/article/22-shortcode-options-pro-only) (article updated 2025-04-28)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Enable calendar controls on a custom post type

Label: `custom_post_type_setup` | automatic response: enabled | threshold: 0.85

For your custom post type, enable Editor and Custom Fields in its Supports settings. When editing with Gutenberg, also enable Show in REST API. This applies to post types registered through tools such as CPTUI, ACF, and Meta Box. In ACF Pro, enable Advanced Configuration to access the Supports settings.

Sources:

- [Use With Custom Post Types](https://docs.piecalendar.com/article/14-use-with-custom-post-types) (article updated 2024-03-21)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Filter events by categories or taxonomy terms

Label: `taxonomy_filter` | automatic response: enabled | threshold: 0.85

In Pro, use taxonomy and terms to filter the event query, for example [piecal taxonomy="category" terms="Concerts"]. Multiple terms can be comma-separated. The operator defaults to IN; documented alternatives include NOT IN, AND, EXISTS, and NOT EXISTS. Use the taxonomy and term values appropriate to your site.

Sources:

- [Shortcode Options [Pro Only]](https://docs.piecalendar.com/article/22-shortcode-options-pro-only) (article updated 2025-04-28)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Page-builder and theme compatibility

Label: `builder_compatibility` | automatic response: enabled | threshold: 0.85

The compatibility guide lists Gutenberg, Classic Editor, Beaver Builder, Elementor, GeneratePress, and Divi as fully compatible. In Oxygen and Bricks, the [piecal] shortcode may not fully render inside the builder, but should render on the front end. Check the live page when the builder preview is incomplete; unresolved issues should go to support.

Sources:

- [Compatibility With Page Builders and Themes](https://docs.piecalendar.com/article/34-compatibility-with-page-builders) (article updated 2024-01-22)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Add the calendar or event-info block

Label: `block_editor` | automatic response: enabled | threshold: 0.85

In the WordPress Block Editor, open the page or post, click Add Block (+), search for Pie Calendar, and select the calendar block. Configure its options in the editor. Use Pie Calendar Event Info for individual event details. To migrate an existing calendar shortcode, add the block, select equivalent settings, and remove that shortcode. Shortcodes remain supported.

Sources:

- [Block Editor Support](https://docs.piecalendar.com/article/71-block-editor-support) (article updated 2025-04-28)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Enable visitor Add to Calendar links

Label: `add_to_calendar` | automatic response: disabled pending more calibration evidence | threshold: 0.99

Add to Calendar links require Pro and are off until enabled. In WordPress go to Settings > Pie Calendar and choose the calendars to show in the event popover. Supported destinations include Google Calendar, Office365, and ICS files for calendars such as Apple and Outlook. On a single-event page, use [piecal-info fragments="atc"] to display only those links.

Sources:

- [Add to Calendar Links](https://docs.piecalendar.com/article/30-add-to-calendar-links) (article updated 2024-10-23)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Understand or disable adaptive time zones

Label: `adaptive_timezone` | automatic response: enabled | threshold: 0.85

The Pro adaptive-time-zone guide explains that event times are converted from the WordPress time zone (Settings > General) to each visitor's detected local time zone, including daylight saving time. To keep the calendar from adapting, use [piecal adaptiveTimeZone=false], or disable the corresponding block control. The visitor's detected zone is displayed below the front-end calendar.

Sources:

- [Adaptive Time Zones](https://docs.piecalendar.com/article/31-adaptive-time-zones) (article updated 2025-05-20)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Show dates and times on individual event pages

Label: `event_info` | automatic response: enabled | threshold: 0.85

Use [piecal-info] or the Pie Calendar Event Info block on a single-event post or template. Select fragments such as start, end, timezone, allday, or all; for example [piecal-info fragments="start, timezone"]. Pro also supports atc for Add to Calendar links. Date/time formatting defaults to WordPress settings and can be overridden using the format attribute with PHP date-format characters.

Sources:

- [Show Event Data on Single Posts with Pie Calendar Info [piecal-info]](https://docs.piecalendar.com/article/85-show-event-data-on-single-posts-piecal-info) (article updated 2026-01-28)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Use existing custom fields for event dates

Label: `custom_date_fields` | automatic response: enabled | threshold: 0.85

The developer guide supports existing date/time meta fields through piecal_event_query_args, piecal_start_date_meta_key, and piecal_end_date_meta_key. Its ACF example assumes Date Time Picker fields with the default return format. This changes the event query: only posts with the designated custom start field appear, and the native start/end controls and Show on Calendar toggle are ignored. Follow the linked example with your field names; site-specific code changes need developer review.

Sources:

- [Use Custom Fields as Event Date & Time](https://docs.piecalendar.com/article/23-use-custom-fields-as-event-date-time) (article updated 2024-09-23)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Set event colors by event or taxonomy

Label: `event_colors` | automatic response: enabled | threshold: 0.85

Pro provides per-event color and text-color options. For automatic colors based on category, taxonomy term, or custom post type, the developer guide uses piecal_event_array_filter to change color and textColor on each event. Use the linked examples as a starting point and adapt the taxonomy, term slugs, post-type slug, and colors to your site.

Sources:

- [Setting Event Colors By Taxonomy Term or CPT](https://docs.piecalendar.com/article/37-setting-event-colors-by-taxonomy-term) (article updated 2024-09-17)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Show featured images in event popovers

Label: `popover_image` | automatic response: enabled | threshold: 0.85

In Pie Calendar Pro 1.3.2 or later, add featuredimage=true to your calendar shortcode, for example [piecal featuredimage=true]. The event uses the post's featured image in its popover. The linked guide also points to the developer approach for adding custom fields to popover content.

Sources:

- [Show Featured Image in Popover](https://docs.piecalendar.com/article/51-show-featured-image-in-popover) (article updated 2024-09-10)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Open the event page or a custom URL directly

Label: `skip_popover` | automatic response: enabled | threshold: 0.85

The documentation provides a developer snippet using piecal_additional_event_click_js to skip the popover and open the event page. For a custom URL field, the separate guide uses piecal_event_array_filter and click JavaScript; its sample assumes ACF. Follow the linked snippet appropriate to the desired destination. Adapting custom PHP/JavaScript to your site should be reviewed by a developer.

Sources:

- [Skip Popover on Event Click](https://docs.piecalendar.com/article/29-skip-popover-on-event-click) (article updated 2025-12-18)
- [Skip Popover and Go To Custom URL Field](https://docs.piecalendar.com/article/48-skip-popover-and-go-to-custom-url-field) (article updated 2025-07-11)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Accept event submissions from site visitors

Label: `frontend_submissions` | automatic response: enabled | threshold: 0.85

Use a capable front-end form plugin that can create WordPress posts and map submitted values to Pie Calendar's event meta fields. The tutorial demonstrates Gravity Forms with its Advanced Post Creation add-on; it also mentions Fluent Forms and WS Forms as alternatives. Map the event flag and correctly formatted date/time fields using the meta-field reference. This is a form-plugin integration, not a built-in submission form.

Sources:

- [Front End Calendar Submissions Tutorial](https://docs.piecalendar.com/article/7-front-end-calendar-submissions-tutorial) (article updated 2023-06-07)
- [Meta Fields](https://docs.piecalendar.com/article/8-meta-fields) (article updated 2025-01-02)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Import events from a spreadsheet or CSV

Label: `csv_import` | automatic response: enabled | threshold: 0.85

Export your spreadsheet as CSV and use an import tool that maps columns to WordPress posts and custom fields; WP All Import Pro is one documented example, not a requirement. Map the post title and Pie Calendar meta fields, including _piecal_is_event with value 1 and the date fields. Follow the meta-field reference for exact formats. Pie Calendar support does not cover third-party import plugins.

Sources:

- [Import a CSV of Events Into Pie Calendar](https://docs.piecalendar.com/article/49-import-a-csv-of-events-into-pie-calendar) (article updated 2024-07-24)
- [Meta Fields](https://docs.piecalendar.com/article/8-meta-fields) (article updated 2025-01-02)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Upgrade to an unlimited-site license

Label: `license_upgrade` | automatic response: enabled | threshold: 0.85

Sign in at https://piecalendar.com/my-account/, choose View Licenses, then View Upgrades beside your license. Select Upgrade License and complete checkout. The guide describes paying the difference to the unlimited-site license and continuing to use the existing license key. For questions about your specific purchase, eligibility, or a failed checkout, contact a human representative.

Sources:

- [Upgrade Your License](https://docs.piecalendar.com/article/20-upgrade-your-license) (article updated 2023-07-10)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Download or update an invoice

Label: `invoice_update` | automatic response: enabled | threshold: 0.85

After purchasing Pro, sign in at https://piecalendar.com/my-account/ and select View Invoice. To edit the billing details or add VAT information, choose Update at the upper right, enter the details, then select Save Billing Details & Generate Invoice. You can then download the updated PDF invoice. A dispute, tax advice, or a problem with a specific charge requires human assistance.

Sources:

- [Add VAT and Billing Info to Your Invoice](https://docs.piecalendar.com/article/45-add-vat-and-billing-info-to-your-invoice) (article updated 2024-05-31)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Display external ICS feeds

Label: `connector_ics` | automatic response: enabled | threshold: 0.85

Install and configure the Pie Calendar Connector add-on to display external ICS feeds. It works with the free Pie Calendar plugin as well as Pro. In the calendar block, expand Event Sources, enable ICS, and paste the feed URL. With a shortcode, use sources="ics" and supply the URL through icsurls; multiple feed URLs can be comma-separated. This imports feed events for display; it is distinct from visitors exporting a single event.

Sources:

- [How to use the Pie Calendar Connector add-on](https://docs.piecalendar.com/article/83-how-to-use-the-pie-calendar-connector-add-on) (article updated 2026-02-25)
- [Setting up ICS Feeds with Pie Calendar Connector for WordPress](https://docs.piecalendar.com/article/91-setting-up-ics-feeds-with-pie-calendar-connector-for-wordpress) (article updated 2026-02-25)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Connect and display Eventbrite events

Label: `connector_eventbrite` | automatic response: enabled | threshold: 0.85

Use the Pie Calendar Connector add-on. Create an Eventbrite API key and copy its private token. In WordPress go to Settings > Pie Calendar Connector, save the token, select your Eventbrite Organization ID, save again, and choose Synchronize Eventbrite Events. Enable Eventbrite under the block's Event Sources, or use [piecal sources="eventbrite"]. Use sources="native, eventbrite" to include native events too. Enter tokens in your admin settings, not in support chat.

Sources:

- [How to use the Pie Calendar Connector add-on](https://docs.piecalendar.com/article/83-how-to-use-the-pie-calendar-connector-add-on) (article updated 2026-02-25)
- [Setting up Eventbrite with Pie Calendar Connector for WordPress](https://docs.piecalendar.com/article/90-setting-up-eventbrite-with-pie-calendar-connector-for-wordpress) (article updated 2026-02-25)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## Keep Eventbrite changes synchronized

Label: `connector_webhooks` | automatic response: disabled pending more calibration evidence | threshold: 0.99

In Eventbrite go to Account Settings > Developer Links > Webhooks and add a webhook with your site's URL followed by /wp-json/piecal-connector/v1/webhook/update. Enable event.created, event.published, event.unpublished, and event.updated. Save and test it; a successful test returns HTTP 200. Updates can take several minutes. For 400/403 responses, inspect the response body; persistent errors need human investigation.

Sources:

- [Setting up Eventbrite with Pie Calendar Connector for WordPress](https://docs.piecalendar.com/article/90-setting-up-eventbrite-with-pie-calendar-connector-for-wordpress) (article updated 2026-02-25)

Review: [ ] Answer correct for supported versions  [ ] Wording approved

## License activation and unauthorized plugin downloads

Label: `license_activation` | automatic response: enabled | threshold: 0.85

Please contact our team at support@piecalendar.com for help with licensing related issues.

Sources:

- Product-owner approved licensing support response (2026-10-10)

Future handoff: `email` — mailto:support@piecalendar.com. No message is sent by the CLI.

Review: approved by product owner

