#!\Perl64\bin\perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;

use My::Base;

# LOGICA
# se sessione aperta -> link to private-menu
# se sessione non aperta -> mostra form
# se sessione non aperta && submit form -> controllo dati
# se sessione non aperta && submit form && dati corretti -> link to private-menu
# se sessione non aperta && submit form && dati non corretti -> form con errore


my $q = new CGI;
my $session = CGI::Session->load();

if(!($session->is_empty())) { # Sessione già aperta
   print "Location: private-menu-cibi.cgi\n\n";
}

else { # Nessuna sessione
   if($q->param('accedi')) { # submit form
      
      my $username = $q->param('username');
      my $password = $q->param('password');

      my $doc = XML::LibXML->new()->parse_file('..\\data\\admins.xml');  # ATTENZIONE path Windows
      
      if ($doc->findnodes("admins/admin[username/text()='$username' and password/text()='$password']")->size eq 1) {
      #if ($username eq 'admin' && $password eq 'admin') { # Dati corretti
      
         my $session = new CGI::Session(undef, $q, {Directory=>File::Spec->tmpdir});
         #my $session = new CGI::Session();
         $session->expire('60m');
         $session->param('username', $username);
         print $session->header(-location=>"private-menu-cibi.cgi");
      }
      else { # Dati non corretti
      
         showForm("Nome utente o password non corretti.");
      }
   }
   else { # form
      showForm('');
   }
}


#----------------SUB---------------------------

sub showForm {

   my $error = $_[0];

   printStartHtmlPublic("Area amministratore", "Area amministratore");
               
   if ($error ne '') {
      print "<p class='error'>$error</p>";
   }
               
   print "<form action=\"login.cgi\" method=\"post\">
                  <fieldset>
                     <div id='legend'>
                        <legend>Login</legend>
                     </div>
                     <label>Username</label>
                     <input type=\"text\" name=\"username\" size=\"25\"/>
                     <label>Password</label>
                     <input type=\"password\" name=\"password\" size=\"25\"/>
                     <input id='submit' type=\"submit\" name=\"accedi\" value=\"Accedi\" />
                  </fieldset>
               </form>
            ";
            
   printEndHtmlPublic();
            
}

exit 0;
