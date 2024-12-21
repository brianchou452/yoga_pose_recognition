import Head from "next/head";
import Image from "next/image";
import Link from "next/link";
import React from "react";

export default function HomePage() {
  const [message, setMessage] = React.useState("No message found");

  React.useEffect(() => {
    window.ipc.on("message", (message: string) => {
      setMessage(message);
    });
  }, []);

  return (
    <React.Fragment>
      <Head>
        <title>Home - Nextron (basic-lang-typescript)</title>
      </Head>
      <div>
        <p>
          ⚡ Electron + Next.js ⚡ -<Link href="/next">Go to next page</Link>
        </p>
        <Image
          src="/images/logo.png"
          alt="Logo image"
          width={256}
          height={256}
        />
      </div>
      <div>
        <button
          onClick={() => {
            window.ipc.send("message", "Hello");
          }}
        >
          Test IPC
        </button>
        <p>{message}</p>
      </div>
      <div>
        <h2>Live Frame</h2>
        <img src="http://127.0.0.1:8000/api/video/frame" alt="Live Frame" />
      </div>
    </React.Fragment>
  );
}
