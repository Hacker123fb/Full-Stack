import { Link } from "react-router-dom";
import { apiRequest } from '../api';

export default function LandingPage() {
  return (
    <div className="bg-slate-50 text-slate-900">
      {/* NAVBAR */}
      <header className="flex items-center justify-between px-10 py-6">
        <Link to="/" className="text-2xl font-bold text-indigo-600">
          Dayflow
        </Link>
        <nav className="space-x-6">
          <Link to="/login" className="text-slate-600 hover:text-indigo-600">
            Login
          </Link>
          <Link
            to="/signup"
            className="rounded-md bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700"
          >
            Get Started
          </Link>
        </nav>
      </header>

      {/* HERO */}
      <section className="mx-auto mt-20 grid max-w-6xl grid-cols-1 items-center gap-12 px-10 md:grid-cols-2">
        <div>
          <h1 className="text-4xl font-bold leading-tight md:text-5xl">
            A smarter way to manage
            <span className="text-indigo-600"> people & work</span>
          </h1>
          <p className="mt-6 text-lg text-slate-600">
            Dayflow is a modern HRMS that simplifies attendance, leave management,
            payroll visibility, and approvals — all in one intuitive platform.
          </p>
          <div className="mt-8 flex gap-4">
            <Link
              to="/signup"
              className="rounded-md bg-indigo-600 px-6 py-3 text-white hover:bg-indigo-700"
            >
              Start Free
            </Link>
            <Link
              to="/login"
              className="rounded-md border border-slate-300 px-6 py-3 hover:bg-slate-100"
            >
              Login
            </Link>
          </div>
        </div>

        <img
          src="https://illustrations.popsy.co/gray/team-work.svg"
          alt="HR illustration"
          className="w-full"
        />
      </section>

      {/* STATS */}
      <section className="mx-auto mt-28 max-w-6xl px-10">
        <div className="grid grid-cols-2 gap-8 text-center md:grid-cols-4">
          <Stat number="1K+" label="Employees Managed" />
          <Stat number="99%" label="Attendance Accuracy" />
          <Stat number="3x" label="Faster Approvals" />
          <Stat number="24/7" label="System Access" />
        </div>
      </section>

      {/* FEATURES */}
      <section className="mx-auto mt-32 max-w-6xl px-10">
        <h2 className="text-center text-3xl font-bold">
          Built for clarity and control
        </h2>
        <p className="mt-4 text-center text-slate-600">
          Everything you need to run HR smoothly — without complexity.
        </p>

        <div className="mt-16 grid gap-16">
          <Feature
            title="Attendance Tracking"
            text="Track daily and weekly attendance with real-time check-in and check-out."
            image="https://illustrations.popsy.co/gray/time-management.svg"
          />
          <Feature
            title="Leave & Time-Off"
            text="Apply, approve, and manage leave requests with full transparency."
            image="https://illustrations.popsy.co/gray/calendar.svg"
            reverse
          />
          <Feature
            title="Role-Based Dashboards"
            text="Employees and HR/Admins get tailored dashboards for secure access."
            image="https://illustrations.popsy.co/gray/security.svg"
          />
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="mx-auto mt-32 max-w-6xl px-10">
        <h2 className="text-center text-3xl font-bold">How Dayflow works</h2>
        <div className="mt-12 grid gap-8 md:grid-cols-3">
          <Step step="1" title="Sign Up" text="Create an account as Employee or HR." />
          <Step step="2" title="Track & Apply" text="Mark attendance or apply for leave." />
          <Step step="3" title="Approve & Manage" text="Admins approve and manage records." />
        </div>
      </section>

      {/* TESTIMONIALS */}
      <section className="mx-auto mt-32 max-w-6xl px-10">
        <h2 className="text-center text-3xl font-bold">What users say</h2>
        <div className="mt-12 grid gap-8 md:grid-cols-3">
          <Testimonial
            name="HR Manager"
            text="Dayflow reduced our manual work drastically. Everything is so clear."
          />
          <Testimonial
            name="Employee"
            text="Marking attendance and applying leave is effortless now."
          />
          <Testimonial
            name="Team Lead"
            text="Approvals are faster and we finally have transparency."
          />
        </div>
      </section>

      {/* FAQ */}
      <section className="mx-auto mt-32 max-w-4xl px-10">
        <h2 className="text-center text-3xl font-bold">FAQs</h2>
        <div className="mt-10 space-y-6">
          <FAQ q="Is Dayflow free to use?" a="Yes, Dayflow offers a free starter version." />
          <FAQ q="Can employees see salary details?" a="Yes, in read-only mode." />
          <FAQ q="Is data secure?" a="Yes, role-based access ensures security." />
        </div>
      </section>

      {/* FINAL CTA */}
      <section className="mt-32 bg-indigo-600 px-10 py-20 text-center text-white">
        <h3 className="text-3xl font-bold">Ready to simplify HR?</h3>
        <p className="mt-4 text-indigo-100">
          Start using Dayflow today and bring clarity to your organization.
        </p>
        <Link
          to="/signup"
          className="mt-8 inline-block rounded-md bg-white px-6 py-3 font-semibold text-indigo-600 hover:bg-indigo-100"
        >
          Get Started Now
        </Link>
      </section>

      {/* FOOTER */}
      <footer className="border-t border-slate-200 px-10 py-6 text-center text-sm text-slate-500">
        © {new Date().getFullYear()} Dayflow. All rights reserved.
      </footer>
    </div>
  );
}

/* ---------- COMPONENTS ---------- */

function Stat({ number, label }: { number: string; label: string }) {
  return (
    <div>
      <p className="text-3xl font-bold text-indigo-600">{number}</p>
      <p className="mt-2 text-slate-600">{label}</p>
    </div>
  );
}

function Feature({
  title,
  text,
  image,
  reverse,
}: {
  title: string;
  text: string;
  image: string;
  reverse?: boolean;
}) {
  return (
    <div
      className={`grid items-center gap-10 md:grid-cols-2 ${
        reverse ? "md:flex-row-reverse" : ""
      }`}
    >
      <img src={image} alt={title} className="mx-auto w-full max-w-md" />
      <div>
        <h3 className="text-2xl font-bold">{title}</h3>
        <p className="mt-4 text-slate-600">{text}</p>
      </div>
    </div>
  );
}

function Step({
  step,
  title,
  text,
}: {
  step: string;
  title: string;
  text: string;
}) {
  return (
    <div className="rounded-xl border bg-white p-6 text-center shadow-sm">
      <div className="mx-auto mb-4 flex h-10 w-10 items-center justify-center rounded-full bg-indigo-600 text-white">
        {step}
      </div>
      <h4 className="font-semibold">{title}</h4>
      <p className="mt-2 text-slate-600">{text}</p>
    </div>
  );
}

function Testimonial({ name, text }: { name: string; text: string }) {
  return (
    <div className="rounded-xl border bg-white p-6 shadow-sm">
      <p className="text-slate-600">“{text}”</p>
      <p className="mt-4 font-semibold">{name}</p>
    </div>
  );
}

function FAQ({ q, a }: { q: string; a: string }) {
  return (
    <div className="rounded-lg border bg-white p-4">
      <p className="font-semibold">{q}</p>
      <p className="mt-2 text-slate-600">{a}</p>
    </div>
  );
}
