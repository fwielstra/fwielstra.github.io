import rss from '@astrojs/rss';
import { SITE_DESCRIPTION, SITE_TITLE } from '../consts';
import { getSortedPosts, postPath } from '../utils/posts';

// Served at /feed.xml, the URL the old Jekyll site used, so existing subscribers keep working.
export async function GET(context) {
	const posts = await getSortedPosts();
	return rss({
		title: SITE_TITLE,
		description: SITE_DESCRIPTION,
		site: context.site,
		items: posts.map((post) => ({
			title: post.data.title,
			description: post.data.description,
			pubDate: post.data.pubDate,
			categories: post.data.tags,
			link: postPath(post),
		})),
	});
}
