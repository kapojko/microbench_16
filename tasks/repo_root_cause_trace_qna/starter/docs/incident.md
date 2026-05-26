# Incident Notes

- Users report that "continue onboarding" sometimes resumes correctly and sometimes sends them to `/onboarding/welcome`.
- The issue happens more often after the user has been idle for a while.
- Product expected pending onboarding sessions to remain resumable as long as the user keeps interacting before the TTL window closes.
- Continue links resolve through the normal route layer rather than a special privileged bypass.
