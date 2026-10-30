import { type CollectionEntry, getCollection } from 'astro:content';

// Posts are named like Jekyll posts (`2015-10-18-moving-servers.md`); keep serving them at
// the URLs Jekyll gave them (`/2015/10/18/moving-servers/`) so existing links keep working.
export function postParams(post: CollectionEntry<'blog'>) {
	const match = post.id.match(/^(\d{4})-(\d{2})-(\d{2})-(.+)$/);
	if (!match) throw new Error(`Post "${post.id}" is not named YYYY-MM-DD-slug`);
	const [, year, month, day, slug] = match;
	return { year, month, day, slug };
}

export function postPath(post: CollectionEntry<'blog'>) {
	const { year, month, day, slug } = postParams(post);
	return `/${year}/${month}/${day}/${slug}/`;
}

export async function getSortedPosts() {
	return (await getCollection('blog')).sort(
		(a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf(),
	);
}
