export type Host = 'claude' | 'codex' | 'factory';

export interface HostPaths {
 skillRoot: string;
 localSkillRoot: string;
 binDir: string;
 browseDir: string;
 designDir: string;
}

export const HOST_PATHS: Record<Host, HostPaths> = {
 claude: {
 skillRoot: '~/.claude/skills/opengstack',
 localSkillRoot: '.claude/skills/opengstack',
 binDir: '~/.claude/skills/opengstack/bin',
 browseDir: '~/.claude/skills/opengstack/browse/dist',
 designDir: '~/.claude/skills/opengstack/design/dist',
 },
 codex: {
 skillRoot: '$OpenGStack_ROOT',
 localSkillRoot: '.agents/skills/opengstack',
 binDir: '$OpenGStack_BIN',
 browseDir: '$OpenGStack_BROWSE',
 designDir: '$OpenGStack_DESIGN',
 },
 factory: {
 skillRoot: '$OpenGStack_ROOT',
 localSkillRoot: '.factory/skills/opengstack',
 binDir: '$OpenGStack_BIN',
 browseDir: '$OpenGStack_BROWSE',
 designDir: '$OpenGStack_DESIGN',
 },
};

export interface TemplateContext {
 skillName: string;
 tmplPath: string;
 benefitsFrom?: string[];
 host: Host;
 paths: HostPaths;
 preambleTier?: number; // 1-4, controls which preamble sections are included
}

/** Resolver function signature. args is populated for parameterized placeholders like {{INVOKE_SKILL:name}}. */
export type ResolverFn = (ctx: TemplateContext, args?: string[]) => string;
