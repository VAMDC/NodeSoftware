.. _addit:

Additional topics
=============================================


.. _gitcollab:

Collaborating with git and GitHub
-----------------------------------

Git is a decentralized version control system (http://git-scm.com/). This 
means among other things that:

* Each checked out copy of the code has the full version history.
* There is no central repository, all repositories ("repos") are equal (but some *can* be made more equal than others, as we'll see below).
* Commits happen locally into your working repo, no network connection needed.
* Repos are updated and synced with each other by pushing and pulling commits back and forth between them. 
* There are web-platforms that offer free web-repositories which
  facilitates syncing and merging. We'll use *GitHub* (http://www.github.com/).

The setup that we want looks like this:

.. image:: gitcollab.png
   :width: 300 px
   :alt: The three repositories and their relation


* The **local repository** (also known as your "working copy") is your own workspace. This is where you do
  all your work. It offers you full local version control without
  necessarily having to upload the changes anywhere. We'll get to how you create your
  local repo in a minute.
* Your **origin** is an online version of your repository, stored online
  at GitHub. When you want to sync the two you need to *push* your
  latest local changes to origin. Once online, others will also be able to see the changes. 
* **Upstream** is a unique repository that serves as an online
  code "central" managed by VAMDC. It too is hosted on
  GitHub. Upstream serves as a convenient way to update your
  distribution; you should regularly *pull* the latest changes into your
  local repo to stay updated. Conversely, if you want your own changes
  to be incoorperated into the central distribution you can send a
  *pull request* to upstream. The relevant commit(s) in your **origin**
  repo will be reviewed and will, if accepted, be merged into upstream
  so that others will get the changes next time they do a pull.
* You can certainly have **several local repositories**, e.g. one on your laptop, 
  one on your desktop and one on the server where the node runs. You 
  then use the online **origin** repository to keep them in sync. For example: You work 
  from your laptop and commit your changes locally. You then push them to 
  your origin repository. Next all you need to do is to tell your other local
  repos to pull from origin and they will all be synced. 
  
Now enough with theory, let's do this in practice. To create your own 
repositories (origin and local) do the following:

* Go to http://github.com and make an account. This includes that you 
  (create and) upload an ssh-key to be able to pull and push securely and 
  without typing your password all the time. Simply follow the instructions
  on GitHub.
* Visit the repository at https://github.com/VAMDC/NodeSoftware and
  klick "fork" in the upper right corner. This will make a copy of the
  original repository under your account. This is your **origin** (see above).
  For more information on forking, you can read http://help.github.com/forking/.
* Github will give you instructions on how to *clone* your origin
  to your own computer, thereby creating a local repo, your **local
  repository**, aka your "working copy". 
* You can repeat the cloning on as many machines as you see fit.
* Tell your local repos where **upstream** is by running the following
  command in each of them: *git remote add upstream git://github.com/VAMDC/NodeSoftware.git* 

Now that you are all set, a typical working session may look like this::

    $ cd $VAMDCROOT               # got to your local repo
    $ git status                  # should tell you you have a clean tree and are on the branch "master"
    $ git pull origin             # pull from your origin, in case you pushed things there from another of your local repos.
    $ git pull upstream           # fetch the latest from upstream and merge it with your tree.
    $ git log                     # read the commit log about what is new.
    $ ....                    # edit your files
    $ git status                  # review which files have changed
    $ git diff                    # review details of your changes
    $ git diff <filename>         # see canges in one file only
    $ git add <filename>          # add a file to be commited with the next commit, e.g. a new file
    $ git commit -a -m "message"  # commit all changed files. ALWAYS check the status before you use -a to prevent that you commit unwanted files.
    $ git commit -m "message" <filenames>   # commit, but include only the named files in the commit    
    $ ....                   # more edits, more commits. until, at the end of day:
    $ git status                  # also tells you how many commits you are ahead of your origin
    $ git push                    # push all commits to your origin, also the new ones that came from upstream.


.. note::
    There are several graphical user interfaces available for git that
    will facilitate overview and some operations for the less 
    command-line adept. Commonly used ones for Linux are *gitk* and *gitg*.
    Good editors also integrate with git so that you can handle the 
    version control from within the editor.

After you pushed your work to your origin, you can go to the *GitHub* 
wesite and send a *pull request* to the upstream repository, if you want 
your changes to be propagated to everybody else. We will then look at 
your commits and merge them.

A few dos and don'ts that are worthwhile to keep in mind with git:

* Do commit often. It goes instantly.
* Pull and push less often, but often enough. You certainly want to pull 
  from upstream before making changes, since you otherwise
  might work on outdated versions of files which
  will result in conflicts later. You also do no want to sit on your
  local commits for too long but push them frequently instead.
* Never pull into a dirty tree (i.e. one that has uncommitted changes). 
  Commit first, then pull. Alternatively read *git help stash*.
* *Git* trusts you know what you are doing. It will allow you to do stupid
  things, too.
* Don't panic. Yes, *git* may have a comparably steep learning curve, but it
  is a powerful tool and all problems can be resolved.



Situations that commonly arise and how to solve them
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Merge conflicts.** When you pull from Upstream into your repo, other's 
changes are merged with yours. It might however happen that someone else 
has changed the same line in the same file as you have in onw of your 
own commits, which results in a merge conflict. The pull commands warns 
you about this and *git status* shows the file in question as "both 
modified". The file itself contains both versions of the conflicting 
lines, clearly marked. Edit the file so that only one version remains 
and remove the markings. Then you simply commit the file (and push).

**Undo a commit.** To undo a commit means exactly that, *not* that any 
of the files change. For example, undoing the last commit leaves you 
with as much uncommitted changes as you had before your last commit. 
None of your edits is reversed. Undoing commits is practical e.g. when 
you have committed too many things at once or unwanted files; or when 
you want to split one commit into several. You undo a commit with *git 
reset --soft <REF>* where <REF> is the commit that should be resetted to 
(i.e. the next-to-last one, if you want to undo your last commit). Common values for <REF> include:

* *HEAD^* - this is the next-to-last
* *HEAD^^* - the one before the next-to-last.
* *HEAD~5* - five commits back
* *111521cb9d3771e636f5f053d3d1048aa7c8852f* - each commit has a long 
  hash number that uniquely identifies it. They can be seen in *git log* 
  and you can give the hash number of the commit that you want to reset to 
  to *git reset*.

**Revert to an earlier version.** If you want to *throw away* your edits 
since a certain commit, you use *git reset --hard*. For example, to 
revert all files to the state that they were in at the last commit (thow 
away uncommitted changes), you do *git reset --hard HEAD*. Similarly to 
the soft reset, you can also specify earlier commits that you want to 
reset to.

**Look at an earlier version.** You can check out any earlier version of 
any file at any time. For example, *git checkout "master@{1 month ago}" 
<filename>"* will give you the version of the file <filename> from a 
month ago. To go back to the latest, you do *git checkout master 
<filename>* ("master" is the name of the default branch where all you 
commits are). Note that the last command can also be used to thow away 
uncommitted changes in a specific file - a more gentle way than the 
reset described above.

You can also skip the <filename> to check out an earlier version of the 
whole repo (*git checkout master* brings you back to the latest). 
Instead of "master@{1 month ago}" you can use any of the <REF> mentioned 
above, or have a look at http://book.git-scm.com/4_git_treeishes.html.

**Make a branch**. Read *git help branch* for this.


Commit guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~

**One thing at a time.** Please commit often and only include things in 
one commit that logically belong together. For example, changes to your 
node and changes to the common library should not be in the same commit 
but committed separately.

**Meaningful commit messages.** This goes together with the previous: If 
you cannot meaningfully summarize the changes you want to commit in onw 
or two lines, your commit is likely to be too large. Try to make the log 
messages meaningful!

**Good code.** Please try to avoid spaghetti-code, write modular, and follow http://www.python.org/dev/peps/pep-0008/

**Pull first.** Before you send a pull request, please make sure that you 
have pulled from upstream. This will make the merging of your code 
easier, since it will be you who needs to resolve potential conflicts 
before you push to your origin again.

The admin of *upstream* (aka the writer of these lines) might be bribed 
and/or convinced to turn a blind eye on violations against any of the above 
points, but he will be very happy if you try to follow them.



The Django admin interface
---------------------------

tbw

Adding more views to your node
--------------------------------

tbw
