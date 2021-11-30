import { Client } from "@notionhq/client";

import dotenv from "dotenv";
dotenv.config();

// console.log(process.env)

const notion = new Client({ auth: process.env.I_TOKEN });

const databaseId = process.env.DB_ID;

async function addItem(title, body_text) {
  try {
    const response = await notion.pages.create({
      parent: { database_id: databaseId },
      properties: {
        title: {
          title: [
            {
              text: {
                content: title,
              },
            },
          ],
        },
      },
      children: [
        {
          object: "block",
          type: "paragraph",
          paragraph: {
            text: [
              {
                type: "text",
                text: {
                  content:
                    body_text,
                },
              },
            ],
          },
        },
      ],
    });
    console.log({response});
    console.log("Success! Entry added.");
  } catch (error) {
    console.error(error.body);
  }
}

// addItem("My title: Yurts in Big Sur, California", "Lacinato kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm.")
const mtitle = "ROI for different ways of improving yourself"
const mbody = `# return on investment in personal productivity

I saw it brought up in how the ROI for learning things in general is much better for those things which you have aptitude and potential for
(https://danluu.com/learn-what/)
it’s not necessarily the case that being well rounded.

The discussion points out:
https://news.ycombinator.com/item?id=28904021

that sometimes it’s your flaws that really matter. The most ROI are the things you hate or are scared of…
> The famous Scott Galloway (whom I had as a b-school professor) made this point like this: if you are a great guy, great father, great boss, etc, but once in a while you get violently drunk and hurt people in your life - THAT thing offsets everything else. You won’t become better by “doubling down” on what you’re already good at, but by fixing this flaw.

I’m not a wife-beater but I do have a big flaw that I’m unable to do these job applications with tenacity. I don’t even know if that would be good ROI but developing the abillity to just do it — or fixing the inability to do so — is important.

[TRUNCATED]`

addItem(mtitle, mbody)

// (async () => {
//   const response = await notion.pages.create({
//     parent: {
//       database_id: databaseId,
//     },
//     icon: {
//       type: "emoji",
//       emoji: "🎉",
//     },
//     cover: {
//       type: "external",
//       external: {
//         url: "https://website.domain/images/image.png",
//       },
//     },
//     properties: {
//       Name: {
//         title: [
//           {
//             text: {
//               content: "Tuscan Kale",
//             },
//           },
//         ],
//       },
//       Description: {
//         text: [
//           {
//             text: {
//               content: "A dark green leafy vegetable",
//             },
//           },
//         ],
//       },
//       "Food group": {
//         select: {
//           name: "🥦 Vegetable",
//         },
//       },
//       Price: {
//         number: 2.5,
//       },
//     },
//     children: [
//       {
//         object: "block",
//         type: "heading_2",
//         heading_2: {
//           text: [
//             {
//               type: "text",
//               text: {
//                 content: "Lacinato kale",
//               },
//             },
//           ],
//         },
//       },
//       {
//         object: "block",
//         type: "paragraph",
//         paragraph: {
//           text: [
//             {
//               type: "text",
//               text: {
//                 content:
//                   "Lacinato kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm.",
//                 link: {
//                   url: "https://en.wikipedia.org/wiki/Lacinato_kale",
//                 },
//               },
//             },
//           ],
//         },
//       },
//     ],
//   });
//   console.log(response);
// })();
