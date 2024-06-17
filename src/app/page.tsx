import { readFile } from "fs/promises";
import styles from "./page.module.css";

type HeadlineURL = {
  title: string,
  url: string,
}

export default async function Home() {
  const data = await readFile("links.json", "utf8");
  const links: HeadlineURL[] = JSON.parse(data);

  return (
    <main className={styles.main}>
      <table className={styles.table}>
        <thead>
          <tr>
            <td><h3>Headline</h3></td>
            <td><h3>Link</h3></td>
          </tr>
        </thead>
        <tbody>
          {links.map((item) => (
            <tr key={0}>
              <td>{item.title}</td>
              <td><a href={item.url}>{item.url}</a></td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
