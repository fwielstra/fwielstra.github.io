---
layout:     post
title:      Implementing temporal tables in SQLite
date:       2022-02-04 13:37:00
summary:    Temporal tables is a feature found in enterprise SQL servers to maintain a history of edits. This post explains how to implement this in SQLite
---

Temporal tables is a technology sometimes found in enterprise SQL servers. It allows a table to maintain a history of edits over time, and by extension, to review the state of a row at any given time in the past. Temporal tables offer a major advantage over maintaining a 'version' column in that it allows querying not just one row, but a set of relationships over time as well. In this post, I will explain some use cases for temporal tables, and how to implement them in SQLite which does not support these by default.

For context, I implemented this in a Go application, but this post is focused on pure SQL so knowledge of Go or any other programming language is not required.

## Challenge

A basic and traditional SQL table has tables and rows of data. This data is either added to (adding new rows through `INSERT`), updated (updating existing rows through `UPDATE`), or removed (`DELETE`). There are, however, a few features in an application that require a developer to break away from this pattern. I will name a few.

### Auditing

Auditing is following how data changed over time - when it was changed, by who, and why. This is sometimes needed for security, or just to review what changed since a certain timestamp. Some systems have auditing as a requirement.

### Restoring History

A more interesting use case is adding the ability to undo a change - either some of the data itself, or even 'undeleting' a row. The last use case is often solved using 'soft deletes', where a table has an additional row like `deleted` or `deleted_at` that indicates that, while the row is still present, it should no longer be usable by a user of the application. Soft deleting a row like this allows reviewing the data, ensuring constraints remain in place (e.g. account name reuse), or undoing the delete operation.

The first use case, restoring data, is where you can roll back a change to a row to a previous version. The reasons to do so are many; in my particular use case, our application is used to manage large and complicated configuration for another application, where this updated configuration may need to be reverted to a previously working version.

How do temporal tables solve this problem? I will explain

## Temporal Tables

A temporal table add timestamp information to a table. This is usually done in a separate table, but can be implemented in the same table - just be aware that primary keys and unique constraints will no longer work as easily. The temporal table adds two timestamps to a row, a `valid_from` and a `valid_to`. These indicate between which timestamps that particular row's data was valid.

```
>.schema users

>.schema users_history
```

When a row is created, `valid_from` is set to the current time, and `valid_to` is undefined. This is the intial version.
When a user then updates this row, the database engine or application will copy the current data and push it on top of the `history` table, setting the `valid_to` column to the current time. The 'live' table is then updated. This is also done when the row is deleted; the last data is pushed onto the `history` table, then the row is deleted.

something something
